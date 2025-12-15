import xml.etree.ElementTree as ET
from xml.dom import minidom # Used for pretty-printing the final XML
from django.conf import settings
from django.utils import timezone
from SerialNumber.models import SerialNumber

# --- Configuration (These should be set in Django's settings.py) ---
# Example: GS1-assigned GLN for your facility
FACILITY_GLN = getattr(settings, 'EPCIS_FACILITY_GLN', 'urn:epc:id:gln:0000000.00000.0')
# Example: Your GS1 Company Prefix
COMPANY_PREFIX = getattr(settings, 'EPCIS_COMPANY_PREFIX', '001234567')

# --- XML Namespace Definitions ---
# The primary namespaces required for an EPCIS 2.0 document
NS = {
    'epcis': "urn:epcglobal:epcis:xsd:2",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
}

class EPCISEventsGenerator:
    """
    Generates EPCIS 2.0 XML documents based on SerialNumber data.
    """
    
    def __init__(self):
        # Register namespaces to ensure they appear correctly in the output
        for prefix, uri in NS.items():
            ET.register_namespace(prefix, uri)

    def _generate_sgtin_uri(self, gtin, serial_number):
        """Converts GTIN and SN into the SGTIN EPC URI format."""
        # Ensure GTIN is 14 digits (padded with leading zero if necessary)
        gtin_14 = str(gtin).zfill(14)
        
        # Split: Company Prefix (first part) and Item Reference (second part, usually 5 digits)
        # Note: The split point depends on your specific Company Prefix length. 
        # Here we use a common structure for demonstration.
        item_reference = gtin_14[8:13] # Example: 5 digits after the prefix/indicator
        
        return f"urn:epc:id:sgtin:{COMPANY_PREFIX}.{item_reference}.{serial_number}"

    def generate_epcis_commissioning(self, serial_number_queryset):
        """
        Generates an EPCIS XML document for the commissioning (printing) event.
        Assumes all S/Ns in the queryset are for the same batch/product.
        
        :param serial_number_queryset: Django QuerySet of SerialNumber objects (in 'PRINTED' status).
        :return: Pretty-printed EPCIS XML string.
        """
        if not serial_number_queryset.exists():
            return None

        # Get metadata from the first SN (assuming batch data is consistent)
        first_sn = serial_number_queryset.first()
        batch_lot = first_sn.batch_lot
        expiration_date = first_sn.expiration_date.strftime('%Y-%m-%d')
        
        # --- 1. Root Element: EPCISDocument ---
        # Use the full namespace URI for the root element
        root = ET.Element(f"{{{NS['epcis']}}}EPCISDocument", 
                          attrib={
                              "schemaVersion": "2.0",
                              "creationDate": timezone.now().isoformat()
                          })

        # --- 2. EPCISBody and EventList ---
        epcis_body = ET.SubElement(root, f"{{{NS['epcis']}}}EPCISBody")
        event_list = ET.SubElement(epcis_body, f"{{{NS['epcis']}}}EventList")

        # --- 3. ObjectEvent (The Event that happened) ---
        object_event = ET.SubElement(event_list, f"{{{NS['epcis']}}}ObjectEvent")
        
        # When
        ET.SubElement(object_event, f"{{{NS['epcis']}}}eventTime").text = timezone.now().isoformat()
        ET.SubElement(object_event, f"{{{NS['epcis']}}}eventTimeZoneOffset").text = "+00:00"
        
        # The What (epcList)
        epc_list = ET.SubElement(object_event, f"{{{NS['epcis']}}}epcList")
        for sn in serial_number_queryset:
            epc_uri = self._generate_sgtin_uri(sn.pool.product_gtin, sn.full_serial_number)
            ET.SubElement(epc_list, f"{{{NS['epcis']}}}epc").text = epc_uri

        # The Why (Action and Business Step)
        ET.SubElement(object_event, f"{{{NS['epcis']}}}action").text = 'ADD'
        ET.SubElement(object_event, f"{{{NS['epcis']}}}bizStep").text = 'urn:epcglobal:cbv:bizstep:commissioning'

        # The Where (bizLocation)
        biz_location = ET.SubElement(object_event, f"{{{NS['epcis']}}}bizLocation")
        ET.SubElement(biz_location, f"{{{NS['epcis']}}}id").text = FACILITY_GLN

        # Contextual Information (ilmd: Item Level Master Data)
        ilmd = ET.SubElement(object_event, f"{{{NS['epcis']}}}ilmd")
        
        # You must use a specific XML namespace for the product data extensions (e.g., lot and expiration)
        # Here we use 'ext' as a placeholder for a custom extension namespace
        ET.register_namespace('ext', "http://yourcompany.com/epcis/ext")
        extension = ET.SubElement(ilmd, f"{{http://yourcompany.com/epcis/ext}}extension")
        
        # Use simple tags for lot and expiration
        ET.SubElement(extension, f"{{http://yourcompany.com/epcis/ext}}lotNumber").text = batch_lot
        ET.SubElement(extension, f"{{http://yourcompany.com/epcis/ext}}expirationDate").text = expiration_date

        # --- 4. Final Formatting ---
        # Use minidom to pretty-print the XML for readability
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

# --- Example Usage (How you would call this after successful consumption) ---
# Assuming you have a list of SerialNumber IDs that were successfully printed:
def generate_commissioning_document(reserved_sn_ids):
    """Fetches the records and generates the EPCIS document."""
    # Find the records that were just marked 'PRINTED'
    queryset = SerialNumber.objects.filter(pk__in=reserved_sn_ids)
    
    # Initialize the generator
    generator = EPCISEventsGenerator()
    
    # Generate the XML
    epcis_xml = generator.generate_epcis_commissioning(queryset)
    
    if epcis_xml:
        # 1. Print it out for inspection
        print("\n--- GENERATED EPCIS COMMISSIONING DOCUMENT ---")
        print(epcis_xml)
        
        # 2. Save it to disk or push it to an EPCIS repository
        # with open(f"epcis_commissioning_{timezone.now().strftime('%Y%m%d%H%M%S')}.xml", "w") as f:
        #     f.write(epcis_xml)
    return epcis_xml

# Note: In a real Django application, you would integrate this into your views.py
# or a signal that fires after the SerialNumber status is successfully updated to 'PRINTED'.