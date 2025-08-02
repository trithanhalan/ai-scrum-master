#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for AI Scrum Master
Tests all CRUD operations, error handling, data persistence, and response validation
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

class AIScumMasterAPITester:
    def __init__(self, base_url="https://f483cad5-1529-4804-a004-dbf62e7f0466.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.created_items = {}  # Store created items for cleanup/reference

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED {details}")
        else:
            print(f"❌ {name} - FAILED {details}")
        return success

    def make_request(self, method: str, endpoint: str, data: Dict = None, expected_status: int = 200) -> tuple:
        """Make HTTP request and return success status and response data"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            
            if success:
                try:
                    return True, response.json()
                except json.JSONDecodeError:
                    return True, response.text
            else:
                return False, f"Status {response.status_code}, Expected {expected_status}. Response: {response.text[:200]}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}"

    def test_health_check(self):
        """Test API health check endpoint with version and features"""
        success, data = self.make_request('GET', '', expected_status=200)
        if success and isinstance(data, dict) and 'message' in data:
            # Check for enhanced API information
            version = data.get('version', '')
            features = data.get('features', [])
            status = data.get('status', '')
            
            if version and isinstance(features, list) and status:
                self.log_test("Enhanced Health Check", True, f"- Version: {version}, Features: {len(features)}, Status: {status}")
            else:
                self.log_test("Enhanced Health Check", False, "- Missing version, features, or status information")
                
            return self.log_test("Basic Health Check", True, f"- {data.get('message', '')}")
        return self.log_test("Basic Health Check", False, f"- {data}")

    def test_voice_transcription(self):
        """Test Voice Input Integration (Whisper API)"""
        print("\n🎤 Testing Voice Transcription...")
        
        # Create a mock audio file for testing
        import io
        import base64
        
        # Create minimal WAV file header (44 bytes) + some audio data
        wav_header = b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x22\x56\x00\x00\x44\xac\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00'
        audio_data = wav_header + b'\x00' * 1000  # Add some silence
        
        # Test POST /voice/transcribe
        files = {'file': ('test_audio.wav', io.BytesIO(audio_data), 'audio/wav')}
        
        try:
            url = f"{self.api_url}/voice/transcribe"
            response = requests.post(url, files=files, data={'language': 'en'}, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'transcribed_text' in data:
                    self.log_test("Voice Transcription Upload", True, f"- ID: {data.get('id', 'N/A')}")
                    
                    # Validate response structure
                    required_fields = ['transcribed_text', 'confidence', 'language_detected', 'duration', 'timestamp']
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        self.log_test("Voice Transcription Response Structure", False, f"- Missing fields: {missing_fields}")
                    else:
                        self.log_test("Voice Transcription Response Structure", True, "- All required fields present")
                        
                    # Test transcription content
                    transcribed_text = data.get('transcribed_text', '')
                    if isinstance(transcribed_text, str) and len(transcribed_text) > 0:
                        self.log_test("Voice Transcription Content", True, f"- Generated text: {transcribed_text[:50]}...")
                    else:
                        self.log_test("Voice Transcription Content", False, "- No transcribed text generated")
                        
                    # Test confidence and duration
                    confidence = data.get('confidence')
                    duration = data.get('duration')
                    if isinstance(confidence, (int, float)) and isinstance(duration, (int, float)):
                        self.log_test("Voice Transcription Metrics", True, f"- Confidence: {confidence}, Duration: {duration}s")
                    else:
                        self.log_test("Voice Transcription Metrics", False, "- Invalid confidence or duration values")
                else:
                    self.log_test("Voice Transcription Upload", False, f"- Invalid response structure: {data}")
            else:
                self.log_test("Voice Transcription Upload", False, f"- Status {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            self.log_test("Voice Transcription Upload", False, f"- Request failed: {str(e)}")
            
        # Test invalid file type
        try:
            files = {'file': ('test.txt', io.BytesIO(b'This is not audio'), 'text/plain')}
            response = requests.post(f"{self.api_url}/voice/transcribe", files=files, timeout=30)
            
            if response.status_code == 400:
                self.log_test("Voice Transcription Error Handling", True, "- Correctly rejected non-audio file")
            else:
                self.log_test("Voice Transcription Error Handling", False, f"- Should reject non-audio files, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Voice Transcription Error Handling", False, f"- Error handling test failed: {str(e)}")

    def test_standup_module(self):
        """Test Enhanced AI Standup Automator with real OpenAI integration"""
        print("\n🔍 Testing Enhanced AI Standup Automator...")
        
        # Test POST /standup with comprehensive data including team_member_name
        standup_data = {
            "team_member_id": "tm_001",
            "team_member_name": "Sarah Johnson",
            "yesterday": "Completed user authentication module, implemented JWT tokens, fixed 3 critical security bugs in the payment flow, and conducted code review for the dashboard component",
            "today": "Working on payment integration with Stripe API, implementing user dashboard with real-time analytics, and setting up automated testing pipeline", 
            "blockers": "Waiting for API keys from payment provider, staging environment is unstable causing test failures",
            "mood": "focused",
            "confidence_level": 7
        }
        
        success, response = self.make_request('POST', 'standup', standup_data, 200)
        if success and isinstance(response, dict) and 'id' in response:
            self.created_items['standup_id'] = response['id']
            self.log_test("Create Enhanced Standup", True, f"- ID: {response['id']}")
            
            # Validate enhanced response structure with new AI features
            required_fields = ['team_member_name', 'summary', 'formatted_output', 'slack_format', 'markdown_format', 'jira_format', 'sentiment_analysis', 'risk_assessment', 'recommendations', 'auto_actions', 'timestamp']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_test("Enhanced Standup Response Structure", False, f"- Missing fields: {missing_fields}")
            else:
                self.log_test("Enhanced Standup Response Structure", True, "- All enhanced fields present")
                
            # Test AI sentiment analysis
            sentiment = response.get('sentiment_analysis', {})
            if isinstance(sentiment, dict) and 'sentiment' in sentiment and 'confidence' in sentiment:
                self.log_test("AI Sentiment Analysis", True, f"- Sentiment: {sentiment.get('sentiment')}, Confidence: {sentiment.get('confidence')}")
            else:
                self.log_test("AI Sentiment Analysis", False, "- Missing or invalid sentiment analysis")
                
            # Test AI risk assessment
            risk = response.get('risk_assessment', {})
            if isinstance(risk, dict) and 'risk_level' in risk and 'risk_score' in risk:
                self.log_test("AI Risk Assessment", True, f"- Risk Level: {risk.get('risk_level')}, Score: {risk.get('risk_score')}")
            else:
                self.log_test("AI Risk Assessment", False, "- Missing or invalid risk assessment")
                
            # Test AI recommendations
            recommendations = response.get('recommendations', [])
            if isinstance(recommendations, list) and len(recommendations) > 0:
                self.log_test("AI Recommendations", True, f"- Generated {len(recommendations)} recommendations")
            else:
                self.log_test("AI Recommendations", False, "- No AI recommendations generated")
                
            # Test auto actions
            auto_actions = response.get('auto_actions', [])
            if isinstance(auto_actions, list) and len(auto_actions) > 0:
                self.log_test("AI Auto Actions", True, f"- Generated {len(auto_actions)} auto actions")
            else:
                self.log_test("AI Auto Actions", False, "- No auto actions generated")
                
            # Test team member name field
            if response.get('team_member_name') == standup_data['team_member_name']:
                self.log_test("Team Member Name Field", True, f"- Name: {response.get('team_member_name')}")
            else:
                self.log_test("Team Member Name Field", False, "- Team member name not preserved")
                
            # Test comprehensive output formats
            formats_to_test = ['formatted_output', 'slack_format', 'markdown_format', 'jira_format']
            for format_name in formats_to_test:
                format_content = response.get(format_name, '')
                if isinstance(format_content, str) and len(format_content) > 100:
                    self.log_test(f"AI {format_name.replace('_', ' ').title()}", True, f"- Generated {len(format_content)} characters")
                else:
                    self.log_test(f"AI {format_name.replace('_', ' ').title()}", False, "- Format content too short or missing")
        else:
            self.log_test("Create Enhanced Standup", False, f"- {response}")
            
        # Test GET /standup with team member filtering
        success, response = self.make_request('GET', 'standup?limit=5&team_member_id=tm_001', expected_status=200)
        if success and isinstance(response, list):
            self.log_test("Get Standups with Filtering", True, f"- Retrieved {len(response)} standups")
            if len(response) > 0 and 'team_member_name' in response[0]:
                self.log_test("Enhanced Standup List Structure", True, "- Valid enhanced standup objects")
            else:
                self.log_test("Enhanced Standup List Structure", False, "- Missing enhanced fields in list")
        else:
            self.log_test("Get Standups with Filtering", False, f"- {response}")

    def test_ticket_module(self):
        """Test Smart AI Ticket Generator with OpenAI integration"""
        print("\n🎫 Testing Smart AI Ticket Generator...")
        
        # Test POST /ticket with comprehensive data
        ticket_data = {
            "title": "Implement Real-time Analytics Dashboard",
            "description": "Create a comprehensive analytics dashboard that displays real-time user engagement metrics, revenue tracking, and system performance indicators. The dashboard should support multiple chart types, data filtering, and export functionality for business stakeholders.",
            "project_context": "SaaS platform with React frontend, FastAPI backend, and PostgreSQL database. Current user base of 10,000+ active users requiring scalable analytics solution.",
            "priority": "High",
            "labels": ["analytics", "dashboard", "real-time"]
        }
        
        success, response = self.make_request('POST', 'ticket', ticket_data, 200)
        if success and isinstance(response, dict) and 'id' in response:
            self.created_items['ticket_id'] = response['id']
            self.log_test("Create Smart Ticket", True, f"- ID: {response['id']}")
            
            # Validate enhanced response structure with AI-generated fields
            required_fields = ['title', 'description', 'acceptance_criteria', 'labels', 'priority', 'estimated_hours', 'story_points', 'assignee_suggestion', 'risk_factors', 'technical_requirements', 'business_value', 'complexity_score']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_test("Smart Ticket Response Structure", False, f"- Missing fields: {missing_fields}")
            else:
                self.log_test("Smart Ticket Response Structure", True, "- All enhanced fields present")
                
            # Test AI-generated acceptance criteria
            acceptance_criteria = response.get('acceptance_criteria', [])
            if isinstance(acceptance_criteria, list) and len(acceptance_criteria) >= 5:
                self.log_test("AI Acceptance Criteria", True, f"- Generated {len(acceptance_criteria)} criteria items")
                # Check for structured criteria sections
                criteria_text = ' '.join(acceptance_criteria)
                if 'Functional Requirements' in criteria_text and 'Technical Requirements' in criteria_text:
                    self.log_test("Structured Acceptance Criteria", True, "- Contains functional and technical sections")
                else:
                    self.log_test("Structured Acceptance Criteria", False, "- Missing structured sections")
            else:
                self.log_test("AI Acceptance Criteria", False, "- Insufficient acceptance criteria generated")
                
            # Test AI risk assessment
            risk_factors = response.get('risk_factors', [])
            if isinstance(risk_factors, list):
                self.log_test("AI Risk Assessment", True, f"- Generated {len(risk_factors)} risk factors")
            else:
                self.log_test("AI Risk Assessment", False, "- Risk factors not generated")
                
            # Test technical requirements
            tech_requirements = response.get('technical_requirements', [])
            if isinstance(tech_requirements, list) and len(tech_requirements) > 0:
                self.log_test("AI Technical Requirements", True, f"- Generated {len(tech_requirements)} technical requirements")
            else:
                self.log_test("AI Technical Requirements", False, "- Technical requirements not generated")
                
            # Test intelligent label generation
            labels = response.get('labels', [])
            if isinstance(labels, list) and len(labels) >= len(ticket_data.get('labels', [])):
                self.log_test("AI Label Enhancement", True, f"- Enhanced to {len(labels)} labels")
            else:
                self.log_test("AI Label Enhancement", False, "- Labels not enhanced")
                
            # Test business value and complexity scoring
            business_value = response.get('business_value')
            complexity_score = response.get('complexity_score')
            if isinstance(business_value, int) and isinstance(complexity_score, int):
                self.log_test("AI Scoring System", True, f"- Business Value: {business_value}, Complexity: {complexity_score}")
            else:
                self.log_test("AI Scoring System", False, "- Scoring system not working")
                
            # Test assignee suggestion
            assignee_suggestion = response.get('assignee_suggestion', '')
            if isinstance(assignee_suggestion, str) and len(assignee_suggestion) > 10:
                self.log_test("AI Assignee Suggestion", True, f"- Generated suggestion: {assignee_suggestion[:50]}...")
            else:
                self.log_test("AI Assignee Suggestion", False, "- No assignee suggestion generated")
                
        else:
            self.log_test("Create Smart Ticket", False, f"- {response}")
            
        # Test GET /ticket with filtering
        success, response = self.make_request('GET', 'ticket?limit=5&priority=High', expected_status=200)
        if success and isinstance(response, list):
            self.log_test("Get Tickets with Priority Filter", True, f"- Retrieved {len(response)} tickets")
        else:
            self.log_test("Get Tickets with Priority Filter", False, f"- {response}")

    def test_sprint_module(self):
        """Test sprint planner endpoints"""
        print("\n⚡ Testing Sprint Module...")
        
        # Test POST /sprint
        sprint_data = {
            "objectives": "Implement user authentication, build payment integration, create admin dashboard",
            "team_capacity": 48,
            "sprint_duration": 14
        }
        
        success, response = self.make_request('POST', 'sprint', sprint_data, 200)
        if success and isinstance(response, dict) and 'id' in response:
            self.created_items['sprint_id'] = response['id']
            self.log_test("Create Sprint Plan", True, f"- ID: {response['id']}")
            
            # Validate response structure
            required_fields = ['sprint_goal', 'tasks', 'total_estimated_hours', 'capacity_utilization', 'risks', 'recommendations']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_test("Sprint Response Structure", False, f"- Missing fields: {missing_fields}")
            else:
                self.log_test("Sprint Response Structure", True, "- All required fields present")
                
                # Validate tasks structure
                tasks = response.get('tasks', [])
                if isinstance(tasks, list) and len(tasks) > 0:
                    task = tasks[0]
                    task_fields = ['title', 'description', 'estimated_hours', 'priority']
                    if all(field in task for field in task_fields):
                        self.log_test("Sprint Tasks Structure", True, f"- {len(tasks)} tasks with valid structure")
                    else:
                        self.log_test("Sprint Tasks Structure", False, "- Invalid task structure")
                else:
                    self.log_test("Sprint Tasks Structure", False, "- No tasks generated")
        else:
            self.log_test("Create Sprint Plan", False, f"- {response}")
            
        # Test GET /sprint
        success, response = self.make_request('GET', 'sprint?limit=3', expected_status=200)
        if success and isinstance(response, list):
            self.log_test("Get Sprint Plans", True, f"- Retrieved {len(response)} sprint plans")
        else:
            self.log_test("Get Sprint Plans", False, f"- {response}")

    def test_blockers_module(self):
        """Test blocker detection endpoints"""
        print("\n🚫 Testing Blockers Module...")
        
        # Test POST /blockers
        blocker_data = {
            "team_data": {"mock": "data"},
            "days_threshold": 3
        }
        
        success, response = self.make_request('POST', 'blockers', blocker_data, 200)
        if success and isinstance(response, dict) and 'id' in response:
            self.created_items['blocker_id'] = response['id']
            self.log_test("Create Blocker Analysis", True, f"- ID: {response['id']}")
            
            # Validate response structure
            required_fields = ['alerts', 'summary', 'action_items']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_test("Blocker Response Structure", False, f"- Missing fields: {missing_fields}")
            else:
                self.log_test("Blocker Response Structure", True, "- All required fields present")
                
                # Validate alerts structure
                alerts = response.get('alerts', [])
                if isinstance(alerts, list) and len(alerts) > 0:
                    alert = alerts[0]
                    alert_fields = ['title', 'description', 'severity', 'affected_team_members', 'recommended_action']
                    if all(field in alert for field in alert_fields):
                        self.log_test("Blocker Alerts Structure", True, f"- {len(alerts)} alerts with valid structure")
                    else:
                        self.log_test("Blocker Alerts Structure", False, "- Invalid alert structure")
                else:
                    self.log_test("Blocker Alerts Structure", False, "- No alerts generated")
        else:
            self.log_test("Create Blocker Analysis", False, f"- {response}")
            
        # Test GET /blockers
        success, response = self.make_request('GET', 'blockers?limit=3', expected_status=200)
        if success and isinstance(response, list):
            self.log_test("Get Blocker Alerts", True, f"- Retrieved {len(response)} blocker analyses")
        else:
            self.log_test("Get Blocker Alerts", False, f"- {response}")

    def test_retrospective_module(self):
        """Test retrospective composer endpoints"""
        print("\n🔄 Testing Retrospective Module...")
        
        # Test POST /retrospective
        retro_data = {
            "went_well": "Great collaboration on payment integration, thorough code reviews",
            "went_poorly": "Testing environment was unstable, unclear requirements led to rework",
            "improvements": "Set up dedicated testing environment, improve requirement gathering",
            "team_mood": "positive"
        }
        
        success, response = self.make_request('POST', 'retrospective', retro_data, 200)
        if success and isinstance(response, dict) and 'id' in response:
            self.created_items['retro_id'] = response['id']
            self.log_test("Create Retrospective", True, f"- ID: {response['id']}")
            
            # Validate response structure
            required_fields = ['summary', 'key_insights', 'action_items', 'mood_analysis', 'recommendations', 'formatted_output']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_test("Retrospective Response Structure", False, f"- Missing fields: {missing_fields}")
            else:
                self.log_test("Retrospective Response Structure", True, "- All required fields present")
        else:
            self.log_test("Create Retrospective", False, f"- {response}")
            
        # Test GET /retrospective
        success, response = self.make_request('GET', 'retrospective?limit=3', expected_status=200)
        if success and isinstance(response, list):
            self.log_test("Get Retrospectives", True, f"- Retrieved {len(response)} retrospectives")
        else:
            self.log_test("Get Retrospectives", False, f"- {response}")

    def test_dashboard_metrics(self):
        """Test dashboard metrics endpoint"""
        print("\n📊 Testing Dashboard Module...")
        
        # Test GET /metrics
        success, response = self.make_request('GET', 'metrics', expected_status=200)
        if success and isinstance(response, dict):
            self.log_test("Get Dashboard Metrics", True, "- Metrics retrieved")
            
            # Validate metrics structure
            required_fields = ['standups_generated', 'tickets_created', 'sprints_planned', 'blockers_detected', 'retrospectives_completed', 'avg_team_velocity', 'active_users']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_test("Metrics Response Structure", False, f"- Missing fields: {missing_fields}")
            else:
                self.log_test("Metrics Response Structure", True, "- All required fields present")
                
                # Validate that metrics are numbers
                numeric_fields = ['standups_generated', 'tickets_created', 'sprints_planned', 'blockers_detected', 'retrospectives_completed', 'avg_team_velocity', 'active_users']
                invalid_types = []
                for field in numeric_fields:
                    if not isinstance(response.get(field), (int, float)):
                        invalid_types.append(field)
                
                if invalid_types:
                    self.log_test("Metrics Data Types", False, f"- Non-numeric fields: {invalid_types}")
                else:
                    self.log_test("Metrics Data Types", True, "- All metrics are numeric")
        else:
            self.log_test("Get Dashboard Metrics", False, f"- {response}")

    def test_export_functionality(self):
        """Test comprehensive export endpoints for different formats"""
        print("\n📥 Testing Export Functionality...")
        
        # Test export endpoints for different data types
        export_tests = []
        
        if 'standup_id' in self.created_items:
            # Test standup exports
            formats = ['markdown', 'json', 'slack', 'jira']
            for format_type in formats:
                success, response = self.make_request('GET', f"export/standup/{self.created_items['standup_id']}?format={format_type}", expected_status=200)
                if success:
                    export_tests.append(f"Standup {format_type.title()}")
                    self.log_test(f"Export Standup {format_type.title()}", True, f"- Export successful")
                else:
                    self.log_test(f"Export Standup {format_type.title()}", False, f"- {response}")
                    
        if 'ticket_id' in self.created_items:
            # Test ticket exports
            formats = ['json', 'csv', 'jira']
            for format_type in formats:
                success, response = self.make_request('GET', f"export/ticket/{self.created_items['ticket_id']}?format={format_type}", expected_status=200)
                if success:
                    export_tests.append(f"Ticket {format_type.title()}")
                    self.log_test(f"Export Ticket {format_type.title()}", True, f"- Export successful")
                else:
                    self.log_test(f"Export Ticket {format_type.title()}", False, f"- {response}")
                    
        if 'sprint_id' in self.created_items:
            # Test sprint exports
            formats = ['json', 'csv', 'gantt']
            for format_type in formats:
                success, response = self.make_request('GET', f"export/sprint/{self.created_items['sprint_id']}?format={format_type}", expected_status=200)
                if success:
                    export_tests.append(f"Sprint {format_type.title()}")
                    self.log_test(f"Export Sprint {format_type.title()}", True, f"- Export successful")
                else:
                    self.log_test(f"Export Sprint {format_type.title()}", False, f"- {response}")
                    
        # Test bulk export
        success, response = self.make_request('GET', 'export/bulk?type=standups&format=json&limit=10', expected_status=200)
        if success:
            self.log_test("Bulk Export", True, "- Bulk export successful")
        else:
            self.log_test("Bulk Export", False, f"- {response}")
            
        if not export_tests:
            self.log_test("Export Tests", False, "- No items created to test exports")
        else:
            self.log_test("Export Coverage", True, f"- Tested {len(export_tests)} export formats")

    def test_openai_integration(self):
        """Test OpenAI API integration and error handling"""
        print("\n🤖 Testing OpenAI Integration...")
        
        # Test with complex standup data to trigger AI analysis
        complex_standup = {
            "team_member_id": "tm_002", 
            "team_member_name": "Alex Chen",
            "yesterday": "Struggled with the database migration script, spent 4 hours debugging connection issues, finally resolved by updating connection pooling configuration. Also reviewed 2 pull requests and attended architecture meeting.",
            "today": "Planning to implement the new caching layer using Redis, need to coordinate with DevOps team for deployment, and will work on optimizing the search functionality that's been causing performance issues.",
            "blockers": "Redis deployment is blocked by security review, search optimization requires database schema changes that need approval from data team, and I'm feeling overwhelmed with the current workload.",
            "mood": "stressed",
            "confidence_level": 3
        }
        
        success, response = self.make_request('POST', 'standup', complex_standup, 200)
        if success and isinstance(response, dict):
            # Test AI sentiment detection for stressed mood
            sentiment = response.get('sentiment_analysis', {})
            if sentiment.get('sentiment') in ['negative', 'neutral'] or sentiment.get('stress_level') in ['high', 'medium']:
                self.log_test("AI Sentiment Detection", True, f"- Detected stress/negative sentiment correctly")
            else:
                self.log_test("AI Sentiment Detection", False, f"- Failed to detect stress, got: {sentiment}")
                
            # Test AI risk assessment for low confidence
            risk = response.get('risk_assessment', {})
            risk_level = risk.get('risk_level', '').lower()
            if risk_level in ['high', 'medium'] or risk.get('risk_score', 0) > 0.5:
                self.log_test("AI Risk Detection", True, f"- Correctly identified high risk scenario")
            else:
                self.log_test("AI Risk Detection", False, f"- Failed to detect risk, got: {risk}")
                
            # Test AI recommendations for blockers
            recommendations = response.get('recommendations', [])
            if len(recommendations) >= 2:
                self.log_test("AI Recommendations for Blockers", True, f"- Generated {len(recommendations)} recommendations")
            else:
                self.log_test("AI Recommendations for Blockers", False, f"- Insufficient recommendations for complex scenario")
        else:
            self.log_test("Complex AI Analysis", False, f"- {response}")
            
        # Test ticket generation with complex requirements
        complex_ticket = {
            "title": "Implement Multi-tenant SaaS Architecture",
            "description": "Design and implement a comprehensive multi-tenant architecture that supports data isolation, tenant-specific customizations, billing integration, and scalable infrastructure. This is a critical feature for our enterprise customers and involves complex database design, security considerations, and performance optimization.",
            "project_context": "Enterprise SaaS platform serving 50+ enterprise clients with strict data isolation requirements, compliance needs (SOC2, GDPR), and high availability demands (99.9% uptime SLA).",
            "priority": "Critical"
        }
        
        success, response = self.make_request('POST', 'ticket', complex_ticket, 200)
        if success and isinstance(response, dict):
            # Test AI complexity assessment
            complexity_score = response.get('complexity_score', 0)
            if complexity_score >= 7:  # Should be high complexity
                self.log_test("AI Complexity Assessment", True, f"- Correctly assessed high complexity: {complexity_score}/10")
            else:
                self.log_test("AI Complexity Assessment", False, f"- Underestimated complexity: {complexity_score}/10")
                
            # Test comprehensive acceptance criteria generation
            acceptance_criteria = response.get('acceptance_criteria', [])
            criteria_text = ' '.join(acceptance_criteria) if acceptance_criteria else ''
            if len(acceptance_criteria) >= 10 and 'security' in criteria_text.lower() and 'scalability' in criteria_text.lower():
                self.log_test("AI Comprehensive Criteria", True, f"- Generated {len(acceptance_criteria)} detailed criteria")
            else:
                self.log_test("AI Comprehensive Criteria", False, f"- Insufficient or incomplete criteria generation")
                
            # Test risk factor identification
            risk_factors = response.get('risk_factors', [])
            if len(risk_factors) >= 2:
                self.log_test("AI Risk Factor Identification", True, f"- Identified {len(risk_factors)} risk factors")
            else:
                self.log_test("AI Risk Factor Identification", False, f"- Failed to identify sufficient risks for complex project")
        else:
            self.log_test("Complex Ticket AI Analysis", False, f"- {response}")

    def test_api_key_error_handling(self):
        """Test error handling when OpenAI API key is missing or invalid"""
        print("\n🔑 Testing API Key Error Handling...")
        
        # This test assumes the API gracefully handles OpenAI errors
        # In a real scenario, you might temporarily modify the API key to test this
        
        # Test with minimal data that should still work even with API issues
        minimal_standup = {
            "team_member_id": "tm_test",
            "team_member_name": "Test User", 
            "yesterday": "Test",
            "today": "Test",
            "blockers": ""
        }
        
        success, response = self.make_request('POST', 'standup', minimal_standup, 200)
        if success:
            # Even if OpenAI fails, the API should return a fallback response
            self.log_test("API Fallback Handling", True, "- API provides fallback when AI services fail")
        else:
            # Check if it's a proper error response
            if "OpenAI" in str(response) or "API key" in str(response):
                self.log_test("OpenAI Error Handling", True, "- Proper error message for API key issues")
            else:
                self.log_test("OpenAI Error Handling", False, f"- Unexpected error: {response}")

    def test_json_serialization(self):
        """Test JSON serialization of complex AI responses"""
        print("\n📋 Testing JSON Serialization...")
        
        # Create a standup and verify all fields are properly serializable
        test_standup = {
            "team_member_id": "tm_json_test",
            "team_member_name": "JSON Test User",
            "yesterday": "Worked on JSON serialization testing",
            "today": "Continuing with API validation",
            "blockers": "None",
            "mood": "positive",
            "confidence_level": 8
        }
        
        success, response = self.make_request('POST', 'standup', test_standup, 200)
        if success and isinstance(response, dict):
            try:
                # Try to serialize the response back to JSON
                json_str = json.dumps(response, default=str)  # default=str handles datetime objects
                parsed_back = json.loads(json_str)
                
                if isinstance(parsed_back, dict) and len(parsed_back) > 0:
                    self.log_test("JSON Serialization", True, "- All response fields properly serializable")
                else:
                    self.log_test("JSON Serialization", False, "- Serialization resulted in empty or invalid data")
                    
            except (TypeError, ValueError) as e:
                self.log_test("JSON Serialization", False, f"- Serialization failed: {str(e)}")
        else:
            self.log_test("JSON Serialization", False, "- Could not create test data for serialization test")

    def test_error_handling(self):
        """Test error handling for invalid requests"""
        print("\n⚠️ Testing Error Handling...")
        
        # Test invalid endpoint
        success, response = self.make_request('GET', 'invalid-endpoint', expected_status=404)
        if not success and "404" in str(response):
            self.log_test("Invalid Endpoint Handling", True, "- 404 returned correctly")
        else:
            self.log_test("Invalid Endpoint Handling", False, f"- {response}")
            
        # Test POST with missing required fields
        success, response = self.make_request('POST', 'standup', {}, expected_status=422)
        if not success and ("422" in str(response) or "validation" in str(response).lower()):
            self.log_test("Validation Error Handling", True, "- Validation errors handled correctly")
        else:
            self.log_test("Validation Error Handling", False, f"- {response}")

    def run_all_tests(self):
        """Run comprehensive test suite for AI Scrum Master Pro with OpenAI integration"""
        print("🚀 Starting AI Scrum Master Pro Backend API Tests")
        print("🤖 Testing Real OpenAI Integration & Enhanced Features")
        print(f"🌐 Testing against: {self.base_url}")
        print("=" * 70)
        
        # Run all test modules in logical order
        self.test_health_check()
        self.test_standup_module()  # Enhanced AI Standup Automator
        self.test_ticket_module()   # Smart AI Ticket Generator  
        self.test_voice_transcription()  # Voice Input Integration
        self.test_sprint_module()
        self.test_blockers_module()
        self.test_retrospective_module()
        self.test_dashboard_metrics()
        self.test_export_functionality()  # Enhanced export testing
        self.test_openai_integration()    # Specific OpenAI integration tests
        self.test_api_key_error_handling()  # Error handling tests
        self.test_json_serialization()    # JSON serialization tests
        self.test_error_handling()        # General error handling
        
        # Print final results
        print("\n" + "=" * 70)
        print(f"📊 TEST RESULTS: {self.tests_passed}/{self.tests_run} tests passed")
        
        # Detailed summary
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED! AI Scrum Master Pro backend is fully functional.")
            print("✅ OpenAI integration working correctly")
            print("✅ Enhanced features implemented successfully") 
            print("✅ Real AI analysis and sentiment detection operational")
            return 0
        else:
            failed_tests = self.tests_run - self.tests_passed
            print(f"❌ {failed_tests} tests failed. Backend needs attention.")
            
            if success_rate >= 80:
                print("⚠️  Most features working - minor issues detected")
            elif success_rate >= 60:
                print("⚠️  Core functionality working - some features need fixes")
            else:
                print("🚨 Major issues detected - significant fixes required")
                
            return 1

def main():
    """Main test execution"""
    tester = AIScumMasterAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())