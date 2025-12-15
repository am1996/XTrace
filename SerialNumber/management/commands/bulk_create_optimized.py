# YourApp/management/commands/bulk_create_optimized.py
import time
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
# Adjust import paths as needed
from SerialNumber.models import SerialNumber 
from SerialNumberPool.service import reserve_pool_state_for_bulk, generate_alphanumeric_serial 

class Command(BaseCommand):
    help = 'Optimized bulk creation of 1M alphanumeric serials using generators and bulk_create.'

    # ... add_arguments method (same as before) ...
    def add_arguments(self, parser):
        parser.add_argument('--pool_id', type=str, required=True)
        parser.add_argument('--quantity', type=int, default=1_000_000)
        parser.add_argument('--length', type=int, default=12)

    def handle(self, *args, **options):
        # --- Configuration ---
        POOL_ID = options['pool_id']
        TOTAL_RECORDS_TARGET = options['quantity']
        SERIAL_LENGTH = options['length']
        BATCH_SIZE = 5000 
        MAX_ATTEMPTS = TOTAL_RECORDS_TARGET * 1 # Safety break for generation loop
        # ---------------------

        self.stdout.write(f"Starting optimized bulk creation for pool '{POOL_ID}'.")
        start_time_total = time.time()
        
        try:
            # 1. RESERVE POOL STATE
            pool = reserve_pool_state_for_bulk(POOL_ID, TOTAL_RECORDS_TARGET)
            
            # 2. GENERATOR AND INSERTION LOOP
            
            # Use a set to track duplicates *within the current bulk operation* only
            # This is essential to prevent IntegrityError during bulk_create itself.
            current_batch_serials = set()
            items_to_create = []
            
            records_created = 0
            generation_attempts = 0
            
            self.stdout.write(f"Generating and inserting in batches of {TOTAL_RECORDS_TARGET:,}...")

            while records_created < TOTAL_RECORDS_TARGET and generation_attempts < MAX_ATTEMPTS:
                
                # Generate serial on the fly using the generator function
                sn_str = generate_alphanumeric_serial(SERIAL_LENGTH)
                generation_attempts += 1
                
                # Skip if already generated in this *current* bulk run (in-memory check)
                if sn_str in current_batch_serials:
                    continue 

                current_batch_serials.add(sn_str)

                item = SerialNumber(
                    full_serial_number=sn_str,
                    pool=pool, 
                    status='ALLOCATED',
                )
                items_to_create.append(item)

                # Execute bulk insert when batch size is reached
                if len(items_to_create) >= BATCH_SIZE:
                    try:
                        # Use ignore_conflicts=True to let the DB silently drop duplicates
                        # (highly recommended for random generation in high-volume systems)
                        inserted_count = len(SerialNumber.objects.bulk_create(
                            items_to_create, 
                            ignore_conflicts=True
                        ))
                        
                        records_created += inserted_count
                        self.stdout.write(f"Inserted {records_created:,} records (Attempts: {generation_attempts:,})")
                        
                    except IntegrityError as e:
                        # Fallback for databases that don't support ignore_conflicts (e.g., older SQLite)
                        self.stdout.write(self.style.ERROR(f"IntegrityError encountered: {e}. Cannot proceed without ignore_conflicts=True support."))
                        break

                    # Reset batch variables
                    items_to_create = [] 
                    current_batch_serials.clear()

            # Insert remaining items
            if items_to_create:
                inserted_count = len(SerialNumber.objects.bulk_create(items_to_create, ignore_conflicts=True))
                records_created += inserted_count

            # 3. REPORTING
            total_time = time.time() - start_time_total
            
            if records_created < TOTAL_RECORDS_TARGET:
                 self.stdout.write(self.style.WARNING(
                    f"WARNING: Only {records_created:,} records created out of target {TOTAL_RECORDS_TARGET:,}. "
                    "This usually means the probability of duplicates is too high (serial length too short) or a conflict occurred."
                ))
            
            self.stdout.write(self.style.SUCCESS(
                f"\nFinished. Total unique records created: {records_created:,} in {total_time:.2f} seconds."
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"A critical error occurred: {e}"))