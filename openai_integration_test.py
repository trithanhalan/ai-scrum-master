#!/usr/bin/env python3
"""
Focused test for OpenAI Integration in AI Scrum Master Pro
Tests the core AI features: Enhanced Standup Automator, Smart Ticket Generator, and Voice Transcription
"""

import requests
import json
from datetime import datetime, timedelta

class OpenAIIntegrationTester:
    def __init__(self):
        self.base_url = "https://f483cad5-1529-4804-a004-dbf62e7f0466.preview.emergentagent.com"
        self.api_url = f"{self.base_url}/api"
        self.tests_passed = 0
        self.tests_total = 0

    def log_test(self, name: str, success: bool, details: str = ""):
        self.tests_total += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED {details}")
        else:
            print(f"❌ {name} - FAILED {details}")
        return success

    def make_request(self, method: str, endpoint: str, data: dict = None):
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            
            return response.status_code == 200, response.json() if response.status_code == 200 else response.text
        except Exception as e:
            return False, str(e)

    def test_enhanced_standup_automator(self):
        """Test Enhanced AI Standup Automator with real OpenAI integration"""
        print("\n🤖 Testing Enhanced AI Standup Automator...")
        
        # Test with realistic team member data
        standup_data = {
            "team_member_id": "dev_001",
            "team_member_name": "Emily Rodriguez",
            "yesterday": "Completed the user authentication refactoring, implemented OAuth2 integration with Google and GitHub, fixed critical security vulnerability in password reset flow, and conducted thorough testing of the new login system. Also reviewed 3 pull requests from team members.",
            "today": "Working on implementing real-time notifications system using WebSockets, need to integrate with our existing message queue, and planning to optimize database queries for the dashboard that's been running slow under high load.",
            "blockers": "The staging environment keeps crashing when testing WebSocket connections, and I'm waiting for the DevOps team to provision additional Redis instances for the notification system. Also feeling a bit overwhelmed with the current sprint workload.",
            "mood": "concerned",
            "confidence_level": 4
        }
        
        success, response = self.make_request('POST', 'standup', standup_data)
        if success and isinstance(response, dict):
            self.log_test("Enhanced Standup Creation", True, f"ID: {response.get('id', 'N/A')}")
            
            # Test team_member_name field
            if response.get('team_member_name') == standup_data['team_member_name']:
                self.log_test("Team Member Name Field", True, f"Name preserved: {response.get('team_member_name')}")
            else:
                self.log_test("Team Member Name Field", False, "Name not preserved correctly")
            
            # Test AI sentiment analysis
            sentiment = response.get('sentiment_analysis', {})
            if isinstance(sentiment, dict) and 'sentiment' in sentiment and 'confidence' in sentiment:
                sentiment_value = sentiment.get('sentiment', '')
                confidence = sentiment.get('confidence', 0)
                self.log_test("Real AI Sentiment Analysis", True, f"Sentiment: {sentiment_value}, Confidence: {confidence}")
                
                # Check if AI detected the concerned mood and blockers
                if sentiment_value in ['negative', 'neutral'] or sentiment.get('stress_level') in ['medium', 'high']:
                    self.log_test("AI Sentiment Detection Accuracy", True, "Correctly detected stress/concern")
                else:
                    self.log_test("AI Sentiment Detection Accuracy", False, f"Missed stress indicators: {sentiment}")
            else:
                self.log_test("Real AI Sentiment Analysis", False, "Sentiment analysis not working")
            
            # Test AI risk assessment
            risk = response.get('risk_assessment', {})
            if isinstance(risk, dict) and 'risk_level' in risk:
                risk_level = risk.get('risk_level', '')
                risk_score = risk.get('risk_score', 0)
                self.log_test("Real AI Risk Assessment", True, f"Risk Level: {risk_level}, Score: {risk_score}")
                
                # Should detect high risk due to blockers and low confidence
                if risk_level.lower() in ['high', 'medium'] or risk_score > 0.5:
                    self.log_test("AI Risk Detection Accuracy", True, "Correctly identified high-risk scenario")
                else:
                    self.log_test("AI Risk Detection Accuracy", False, f"Underestimated risk: {risk}")
            else:
                self.log_test("Real AI Risk Assessment", False, "Risk assessment not working")
            
            # Test AI recommendations
            recommendations = response.get('recommendations', [])
            if isinstance(recommendations, list) and len(recommendations) >= 2:
                self.log_test("AI Recommendations Generation", True, f"Generated {len(recommendations)} recommendations")
                
                # Check if recommendations are relevant to blockers
                rec_text = ' '.join(recommendations).lower()
                if 'environment' in rec_text or 'devops' in rec_text or 'workload' in rec_text:
                    self.log_test("AI Recommendation Relevance", True, "Recommendations address specific blockers")
                else:
                    self.log_test("AI Recommendation Relevance", False, "Recommendations seem generic")
            else:
                self.log_test("AI Recommendations Generation", False, "Insufficient recommendations generated")
            
            # Test comprehensive output formats
            formats = ['formatted_output', 'slack_format', 'markdown_format', 'jira_format']
            for format_name in formats:
                content = response.get(format_name, '')
                if isinstance(content, str) and len(content) > 200:
                    self.log_test(f"AI {format_name.replace('_', ' ').title()}", True, f"{len(content)} chars")
                else:
                    self.log_test(f"AI {format_name.replace('_', ' ').title()}", False, "Content too short")
        else:
            self.log_test("Enhanced Standup Creation", False, f"Request failed: {response}")

    def test_smart_ticket_generator(self):
        """Test Smart AI Ticket Generator with OpenAI integration"""
        print("\n🎫 Testing Smart AI Ticket Generator...")
        
        # Test with complex, realistic ticket requirements
        ticket_data = {
            "title": "Implement Advanced Analytics Dashboard with Real-time Data Visualization",
            "description": "Design and develop a comprehensive analytics dashboard that provides real-time insights into user behavior, system performance, and business metrics. The dashboard should support multiple visualization types (charts, graphs, heatmaps), allow for custom date ranges, provide drill-down capabilities, and include export functionality for reports. This is a high-priority feature requested by multiple enterprise clients and needs to handle large datasets efficiently while maintaining responsive user experience.",
            "project_context": "Enterprise SaaS platform with 100,000+ active users, processing 1M+ events daily. Current tech stack includes React frontend, FastAPI backend, PostgreSQL database, and Redis for caching. The dashboard will be used by C-level executives, product managers, and data analysts. Must comply with SOC2 and GDPR requirements.",
            "priority": "High",
            "labels": ["analytics", "dashboard", "enterprise", "real-time"]
        }
        
        success, response = self.make_request('POST', 'ticket', ticket_data)
        if success and isinstance(response, dict):
            self.log_test("Smart Ticket Creation", True, f"ID: {response.get('id', 'N/A')}")
            
            # Test AI-generated acceptance criteria
            acceptance_criteria = response.get('acceptance_criteria', [])
            if isinstance(acceptance_criteria, list) and len(acceptance_criteria) >= 10:
                self.log_test("AI Acceptance Criteria Generation", True, f"Generated {len(acceptance_criteria)} criteria")
                
                # Check for structured sections
                criteria_text = ' '.join(acceptance_criteria)
                required_sections = ['Functional Requirements', 'Technical Requirements', 'Quality Requirements']
                sections_found = sum(1 for section in required_sections if section in criteria_text)
                
                if sections_found >= 2:
                    self.log_test("Structured Acceptance Criteria", True, f"Found {sections_found}/3 required sections")
                else:
                    self.log_test("Structured Acceptance Criteria", False, f"Only found {sections_found}/3 sections")
            else:
                self.log_test("AI Acceptance Criteria Generation", False, "Insufficient criteria generated")
            
            # Test AI risk assessment for tickets
            risk_factors = response.get('risk_factors', [])
            if isinstance(risk_factors, list):
                self.log_test("AI Risk Factor Identification", True, f"Identified {len(risk_factors)} risk factors")
                
                # For complex enterprise feature, should identify risks
                if len(risk_factors) >= 1:
                    self.log_test("AI Risk Assessment Accuracy", True, "Identified risks for complex feature")
                else:
                    self.log_test("AI Risk Assessment Accuracy", False, "No risks identified for complex feature")
            else:
                self.log_test("AI Risk Factor Identification", False, "Risk factors not generated")
            
            # Test technical requirements generation
            tech_requirements = response.get('technical_requirements', [])
            if isinstance(tech_requirements, list) and len(tech_requirements) >= 3:
                self.log_test("AI Technical Requirements", True, f"Generated {len(tech_requirements)} requirements")
            else:
                self.log_test("AI Technical Requirements", False, "Insufficient technical requirements")
            
            # Test intelligent complexity and effort estimation
            complexity_score = response.get('complexity_score', 0)
            estimated_hours = response.get('estimated_hours', 0)
            story_points = response.get('story_points', 0)
            
            # Complex enterprise dashboard should have high complexity
            if complexity_score >= 6 and estimated_hours >= 20 and story_points >= 5:
                self.log_test("AI Complexity Assessment", True, f"Complexity: {complexity_score}, Hours: {estimated_hours}, Points: {story_points}")
            else:
                self.log_test("AI Complexity Assessment", False, f"Underestimated complexity: {complexity_score}/10")
            
            # Test business value assessment
            business_value = response.get('business_value', 0)
            if business_value >= 7:  # Enterprise feature should have high business value
                self.log_test("AI Business Value Assessment", True, f"Business Value: {business_value}/10")
            else:
                self.log_test("AI Business Value Assessment", False, f"Underestimated business value: {business_value}/10")
            
            # Test label enhancement
            original_labels = set(ticket_data.get('labels', []))
            enhanced_labels = set(response.get('labels', []))
            if len(enhanced_labels) > len(original_labels):
                self.log_test("AI Label Enhancement", True, f"Enhanced from {len(original_labels)} to {len(enhanced_labels)} labels")
            else:
                self.log_test("AI Label Enhancement", False, "Labels not enhanced by AI")
        else:
            self.log_test("Smart Ticket Creation", False, f"Request failed: {response}")

    def test_voice_transcription(self):
        """Test Voice Input Integration (Whisper API simulation)"""
        print("\n🎤 Testing Voice Input Integration...")
        
        # Create a mock audio file for testing
        import io
        
        # Create minimal WAV file for testing
        wav_header = b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x22\x56\x00\x00\x44\xac\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00'
        audio_data = wav_header + b'\x00' * 2000  # Add some audio data
        
        try:
            files = {'file': ('standup_audio.wav', io.BytesIO(audio_data), 'audio/wav')}
            response = requests.post(f"{self.api_url}/voice/transcribe", files=files, data={'language': 'en'}, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Voice Transcription Upload", True, f"ID: {data.get('id', 'N/A')}")
                
                # Test response structure
                required_fields = ['transcribed_text', 'confidence', 'language_detected', 'duration']
                missing_fields = [field for field in required_fields if field not in data]
                if not missing_fields:
                    self.log_test("Voice Transcription Structure", True, "All required fields present")
                    
                    # Test transcription content (mock implementation)
                    transcribed_text = data.get('transcribed_text', '')
                    if len(transcribed_text) > 10:
                        self.log_test("Voice Transcription Content", True, f"Generated: {transcribed_text[:50]}...")
                    else:
                        self.log_test("Voice Transcription Content", False, "No transcription generated")
                else:
                    self.log_test("Voice Transcription Structure", False, f"Missing: {missing_fields}")
            else:
                self.log_test("Voice Transcription Upload", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Voice Transcription Upload", False, f"Error: {str(e)}")

    def test_api_health_and_features(self):
        """Test API health endpoint with version and features"""
        print("\n🏥 Testing API Health and Features...")
        
        success, response = self.make_request('GET', '')
        if success and isinstance(response, dict):
            # Test version information
            version = response.get('version', '')
            if version and '2.0' in version:
                self.log_test("API Version Check", True, f"Version: {version}")
            else:
                self.log_test("API Version Check", False, f"Unexpected version: {version}")
            
            # Test features list
            features = response.get('features', [])
            expected_features = ['Advanced Analytics', 'JIRA Integration', 'Slack Integration']
            if isinstance(features, list) and len(features) >= 3:
                self.log_test("API Features List", True, f"Features: {', '.join(features)}")
            else:
                self.log_test("API Features List", False, f"Insufficient features: {features}")
            
            # Test operational status
            status = response.get('status', '')
            if status == 'operational':
                self.log_test("API Operational Status", True, f"Status: {status}")
            else:
                self.log_test("API Operational Status", False, f"Status: {status}")
        else:
            self.log_test("API Health Check", False, f"Health check failed: {response}")

    def run_focused_tests(self):
        """Run focused tests on OpenAI integration features"""
        print("🚀 AI Scrum Master Pro - OpenAI Integration Test")
        print("🎯 Focus: Enhanced Standup Automator, Smart Ticket Generator, Voice Transcription")
        print("=" * 80)
        
        self.test_api_health_and_features()
        self.test_enhanced_standup_automator()
        self.test_smart_ticket_generator()
        self.test_voice_transcription()
        
        print("\n" + "=" * 80)
        print(f"📊 OPENAI INTEGRATION TEST RESULTS: {self.tests_passed}/{self.tests_total} tests passed")
        
        success_rate = (self.tests_passed / self.tests_total * 100) if self.tests_total > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! OpenAI integration is working perfectly")
            print("✅ Real AI analysis and sentiment detection operational")
            print("✅ Enhanced features implemented successfully")
        elif success_rate >= 75:
            print("✅ GOOD! OpenAI integration is mostly working")
            print("⚠️  Minor issues detected - core functionality operational")
        elif success_rate >= 50:
            print("⚠️  PARTIAL! Some OpenAI features working")
            print("🔧 Several features need attention")
        else:
            print("❌ CRITICAL! Major OpenAI integration issues")
            print("🚨 Significant fixes required")
        
        return 0 if success_rate >= 75 else 1

if __name__ == "__main__":
    tester = OpenAIIntegrationTester()
    exit_code = tester.run_focused_tests()
    exit(exit_code)