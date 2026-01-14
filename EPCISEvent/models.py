import uuid
import json
from django.db import models
from django.utils import timezone
import xml.etree.ElementTree as ET
from xml.dom import minidom

class EPCISEvent(models.Model):
    # EPCIS 2.0 Event Types
    EVENT_TYPES = [
        ('ObjectEvent', 'Object Event'),
        ('AggregationEvent', 'Aggregation Event'),
        ('TransactionEvent', 'Transaction Event'),
        ('TransformationEvent', 'Transformation Event'),
        ('AssociationEvent', 'Association Event'),
    ]

    # EPCIS Actions
    ACTIONS = [
        ('OBSERVE', 'Observe'),
        ('ADD', 'Add'),      
        ('DELETE', 'Delete'),  
    ]

    # Fields
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default='ObjectEvent')
    event_time = models.DateTimeField(default=timezone.now)
    event_timezone_offset = models.CharField(max_length=6, default="+00:00")
    
    action = models.CharField(max_length=10, choices=ACTIONS, default='OBSERVE')
    biz_step = models.CharField(max_length=100)  # e.g., 'receiving', 'shipping'
    disposition = models.CharField(max_length=100) # e.g., 'in_transit'
    
    # Identifiers (Should be stored as GS1 Digital Links or URNs)
    read_point = models.CharField(max_length=255, help_text="SGLN for the read point")
    biz_location = models.CharField(max_length=255, help_text="SGLN for the business location")
    
    # EPCs should be stored in a way that allows list conversion
    epc_list = models.TextField(help_text="Comma-separated GS1 Digital Links or URNs")

    def get_epcis_json(self):
        """Generates a strictly compliant EPCIS 2.0 JSON-LD document."""
        
        # 1. Define the context (Required for JSON-LD)
        context = "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld"
        
        # 2. Build the event structure
        event_data = {
            "type": self.event_type, # e.g., "ObjectEvent"
            "eventID": f"urn:uuid:{self.event_id}",
            "eventTime": self.event_time.isoformat(),
            "eventTimeZoneOffset": self.event_timezone_offset,
            "action": self.action, # Must be OBSERVE, ADD, or DELETE
            
            # 'Why' - Using URNs to ensure no 404 errors
            "bizStep": f"urn:epcglobal:cbv:bizstep:{self.biz_step}",
            "disposition": f"urn:epcglobal:cbv:disp:{self.disposition}",
            
            # 'What' - Standard EPC list
            "epcList": [epc.strip() for epc in self.epc_list.split(',')],
            
            # 'Where' - SGLN (Global Location Number) 
            # Using the GS1 Digital Link URI format for locations
            "readPoint": {"id": f"https://id.gs1.org/414/{self.read_point}"},
            "bizLocation": {"id": f"https://id.gs1.org/414/{self.biz_location}"}
        }

        # 3. Wrap in an EPCISDocument (The compliant envelope)
        epcis_document = {
            "@context": context,
            "type": "EPCISDocument",
            "schemaVersion": "2.0",
            "creationDate": timezone.now().isoformat(),
            "epcisBody": {
                "eventList": [event_data]
            }
        }
        
        return json.dumps(epcis_document, indent=4)
    def to_epcis_xml(self):
        """Generates a strictly compliant EPCIS 2.0 XML Document."""
        
        # 1. Define Namespaces
        NS_EPCIS = "urn:epcglobal:epcis:xsd:2"
        NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
        NS_CBVMDA = "urn:epcglobal:cbv:mda"
        
        ET.register_namespace('epcis', NS_EPCIS)
        ET.register_namespace('xsi', NS_XSI)
        
        # 2. Root: EPCISDocument
        root = ET.Element(f"{{{NS_EPCIS}}}EPCISDocument", {
            "schemaVersion": "2.0",
            "creationDate": timezone.now().isoformat(),
            f"{{{NS_XSI}}}schemaLocation": f"{NS_EPCIS} http://www.gs1.org/standards/epcis/EPCIS_2_0.xsd"
        })

        # 3. EPCISBody and EventList
        body = ET.SubElement(root, "EPCISBody")
        event_list = ET.SubElement(body, "EventList")
        
        # 4. The Specific Event (ObjectEvent, AggregationEvent, etc.)
        event = ET.SubElement(event_list, self.event_type)
        
        # Required v2 Elements
        ET.SubElement(event, "eventTime").text = self.event_time.isoformat()
        ET.SubElement(event, "eventTimeZoneOffset").text = self.event_timezone_offset
        ET.SubElement(event, "eventID").text = f"urn:uuid:{self.event_id}"
        
        # What: epcList
        epc_list_container = ET.SubElement(event, "epcList")
        for epc in self.epc_list.split(','):
            ET.SubElement(epc_list_container, "epc").text = epc.strip()
        
        # Action (Required)
        ET.SubElement(event, "action").text = self.action
        
        # Why: bizStep and disposition (Using CBV 2.0 URIs)
        ET.SubElement(event, "bizStep").text = f"https://ref.gs1.org/cbv/bizstep/{self.biz_step}"
        ET.SubElement(event, "disposition").text = f"https://ref.gs1.org/cbv/disp/{self.disposition}"
        
        # Where: readPoint and bizLocation
        read_point_id = ET.SubElement(ET.SubElement(event, "readPoint"), "id")
        read_point_id.text = f"urn:epc:id:sgln:{self.read_point}"
        
        biz_loc_id = ET.SubElement(ET.SubElement(event, "bizLocation"), "id")
        biz_loc_id.text = f"urn:epc:id:sgln:{self.biz_location}"

        # 5. Format and Return
        xml_str = ET.tostring(root, encoding='utf-8')
        return minidom.parseString(xml_str).toprettyxml(indent="  ")