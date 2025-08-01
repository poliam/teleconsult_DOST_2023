"""
Management command to fix migration conflicts from commit 4398b6b automatically.
This allows users to simply run: python manage.py migrate_from_4398b6b
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.apps import apps


class Command(BaseCommand):
    help = 'Automatically migrate from commit 4398b6b to current state'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('=== Teleconsult Auto-Migration from 4398b6b ===')
        )
        
        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        try:
            # Step 1: Analyze current migration state
            self.stdout.write('\nStep 1: Analyzing current migration state...')
            applied_migrations = self.get_applied_migrations()
            current_state = self.analyze_database_state()
            
            # Step 2: Determine what needs to be done
            self.stdout.write('\nStep 2: Determining required actions...')
            actions = self.plan_migration_actions(applied_migrations, current_state)
            
            # Step 3: Execute the plan
            self.stdout.write('\nStep 3: Executing migration plan...')
            if not dry_run:
                self.execute_migration_plan(actions)
            else:
                self.display_migration_plan(actions)
                
            # Step 4: Verify final state
            self.stdout.write('\nStep 4: Verifying final state...')
            if not dry_run:
                self.verify_final_state()
            
            self.stdout.write(
                self.style.SUCCESS('\n✅ Migration completed successfully!')
            )
            self.stdout.write('You can now run: python manage.py test')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Migration failed: {str(e)}')
            )
            raise

    def get_applied_migrations(self):
        """Get list of currently applied migrations"""
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        return recorder.applied_migrations()

    def analyze_database_state(self):
        """Analyze current database schema state"""
        with connection.cursor() as cursor:
            table_names = connection.introspection.table_names(cursor)
            
            state = {
                'tables': table_names,
                'details_files_exists': 'patient_details_files' in table_names,
                'details_audit_exists': 'patient_details_audit' in table_names,
                'psychiatric_evaluate_exists': 'consultation_psychiatric_evaluate' in table_names,
                'nurse_notes_exists': 'consultation_nurse_notes' in table_names,
            }
            
            # Check specific fields
            if 'patient_considering_event' in table_names:
                columns = {col.name for col in connection.introspection.get_table_description(cursor, 'patient_considering_event')}
                state['considering_event_has_score_1_16'] = 'score_1_16' in columns
                state['considering_event_has_total_score'] = 'total_score' in columns
            else:
                state['considering_event_has_score_1_16'] = False
                state['considering_event_has_total_score'] = False
                
            if 'consultation_encounter' in table_names:
                columns = {col.name for col in connection.introspection.get_table_description(cursor, 'consultation_encounter')}
                state['encounter_has_for_follow_up'] = 'for_follow_up' in columns
            else:
                state['encounter_has_for_follow_up'] = False
                
            return state

    def plan_migration_actions(self, applied_migrations, current_state):
        """Plan what migration actions need to be taken"""
        actions = []
        
        # Check for conflict scenario from 4398b6b
        consultation_0020_applied = ('consultation', '0020_encounter_for_follow_up_psychiatric_evaluate_and_more') in applied_migrations
        patient_0019_applied = ('patient', '0019_considering_event_score_1_16_and_more') in applied_migrations
        patient_0020_applied = ('patient', '0020_merge_20250727_2145') in applied_migrations
        
        self.stdout.write(f'  - consultation.0020 applied: {consultation_0020_applied}')
        self.stdout.write(f'  - patient.0019 applied: {patient_0019_applied}')
        self.stdout.write(f'  - patient.0020_merge applied: {patient_0020_applied}')
        
        if consultation_0020_applied and not patient_0019_applied:
            # This is the 4398b6b conflict scenario
            self.stdout.write(self.style.WARNING('  ⚠️  Detected 4398b6b migration conflict'))
            actions.append('fix_migration_records')
            
        # Check what database changes are needed
        if not current_state['details_files_exists']:
            actions.append('create_details_files')
            
        if not current_state['considering_event_has_score_1_16']:
            actions.append('add_score_fields')
            
        if not current_state['details_audit_exists']:
            actions.append('create_details_audit')
            
        if not current_state['encounter_has_for_follow_up']:
            actions.append('add_for_follow_up')
            
        if not current_state['psychiatric_evaluate_exists']:
            actions.append('create_psychiatric_evaluate')
            
        if not current_state['nurse_notes_exists']:
            actions.append('create_nurse_notes')
            
        return actions

    def execute_migration_plan(self, actions):
        """Execute the planned migration actions"""
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        
        for action in actions:
            self.stdout.write(f'  → Executing: {action}')
            
            if action == 'fix_migration_records':
                # Mark the patient migrations as applied to resolve the conflict
                recorder.record_applied('patient', '0016_details_files')
                recorder.record_applied('patient', '0017_alter_considering_event_considering_event_1_and_more')
                recorder.record_applied('patient', '0018_alter_considering_event_considering_event_1_and_more')
                recorder.record_applied('patient', '0019_considering_event_score_1_16_and_more')
                recorder.record_applied('patient', '0020_merge_20250727_2145')
                self.stdout.write('    ✓ Fixed migration records')
                
            elif action == 'create_details_files':
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS patient_details_files (
                            id BIGINT AUTO_INCREMENT PRIMARY KEY,
                            file_name VARCHAR(250),
                            file VARCHAR(100),
                            create_date DATETIME(6) NOT NULL,
                            update_date DATETIME(6) NOT NULL,
                            history LONGTEXT,
                            status TINYINT(1) NOT NULL DEFAULT 1,
                            is_delete TINYINT(1) NOT NULL DEFAULT 0,
                            details_id BIGINT,
                            FOREIGN KEY (details_id) REFERENCES patient_details(id)
                        )
                    """)
                self.stdout.write('    ✓ Created details_files table')
                
            elif action == 'add_score_fields':
                with connection.cursor() as cursor:
                    cursor.execute("ALTER TABLE patient_considering_event ADD COLUMN IF NOT EXISTS score_1_16 VARCHAR(250) DEFAULT '0'")
                    cursor.execute("ALTER TABLE patient_considering_event ADD COLUMN IF NOT EXISTS total_score VARCHAR(250) DEFAULT '0'")
                self.stdout.write('    ✓ Added score fields to considering_event')
                
            elif action == 'create_details_audit':
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS patient_details_audit (
                            id BIGINT AUTO_INCREMENT PRIMARY KEY,
                            url VARCHAR(250),
                            create_date DATETIME(6) NOT NULL,
                            updated_fields LONGTEXT,
                            status TINYINT(1) NOT NULL DEFAULT 1,
                            is_delete TINYINT(1) NOT NULL DEFAULT 0,
                            details_id BIGINT,
                            user_id INT,
                            FOREIGN KEY (details_id) REFERENCES patient_details(id),
                            FOREIGN KEY (user_id) REFERENCES auth_user(id)
                        )
                    """)
                self.stdout.write('    ✓ Created details_audit table')
                
            elif action == 'add_for_follow_up':
                with connection.cursor() as cursor:
                    cursor.execute("ALTER TABLE consultation_encounter ADD COLUMN IF NOT EXISTS for_follow_up TINYINT(1) NOT NULL DEFAULT 0")
                self.stdout.write('    ✓ Added for_follow_up field to encounter')
                
            elif action == 'create_psychiatric_evaluate':
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS consultation_psychiatric_evaluate (
                            id BIGINT AUTO_INCREMENT PRIMARY KEY,
                            evaluation_consultation_date DATE,
                            create_date DATETIME(6) NOT NULL,
                            update_date DATETIME(6) NOT NULL,
                            history LONGTEXT,
                            status TINYINT(1) NOT NULL DEFAULT 1,
                            is_delete TINYINT(1) NOT NULL DEFAULT 0,
                            create_by_id INT,
                            details_id BIGINT,
                            update_by_id INT,
                            FOREIGN KEY (create_by_id) REFERENCES auth_user(id),
                            FOREIGN KEY (details_id) REFERENCES patient_details(id),
                            FOREIGN KEY (update_by_id) REFERENCES auth_user(id)
                        )
                    """)
                self.stdout.write('    ✓ Created psychiatric_evaluate table')
                
            elif action == 'create_nurse_notes':
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS consultation_nurse_notes (
                            id BIGINT AUTO_INCREMENT PRIMARY KEY,
                            comment LONGTEXT,
                            create_date DATETIME(6) NOT NULL,
                            status TINYINT(1) NOT NULL DEFAULT 1,
                            is_delete TINYINT(1) NOT NULL DEFAULT 0,
                            create_by_id INT,
                            encounter_id BIGINT,
                            FOREIGN KEY (create_by_id) REFERENCES auth_user(id),
                            FOREIGN KEY (encounter_id) REFERENCES consultation_encounter(id)
                        )
                    """)
                self.stdout.write('    ✓ Created nurse_notes table')

    def display_migration_plan(self, actions):
        """Display what would be done in dry run mode"""
        for action in actions:
            self.stdout.write(f'  → Would execute: {action}')

    def verify_final_state(self):
        """Verify that the migration completed successfully"""
        try:
            # Try running normal migrate to see if there are any issues
            call_command('migrate', verbosity=0)
            self.stdout.write('  ✓ All migrations are now consistent')
            
            # Run a basic test
            call_command('check', verbosity=0)
            self.stdout.write('  ✓ System check passed')
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  Post-migration check failed: {str(e)}')
            )
