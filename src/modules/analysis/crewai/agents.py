"""
CrewAI Agents for Legal Analysis

Defines specialized agents that work together to perform comprehensive legal document analysis.
Each agent has a specific role and uses appropriate tools to accomplish legal analysis tasks.
"""

import logging
import json
from typing import Dict, List, Optional, Any
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

from .tools import (
    LegalContextExtractionTool,
    SubjectSynthesisTool,
    StructuredSummaryTool,
    DocumentArticleAnalysisTool,
    QuestionGenerationTool,
    LegalAssessmentTool,
    ConstitutionalRetrievalTool,
    QuestionAnsweringTool
)


class LegalAnalysisCrewManager:
    """
    Manages a crew of specialized legal analysis agents.
    
    This is the main orchestrator that coordinates different agents to perform
    comprehensive legal document analysis using CrewAI framework.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the legal analysis crew manager.
        
        Args:
            openai_api_key: OpenAI API key for model access
            model_name: OpenAI model to use (default: gpt-3.5-turbo)
        """
        self.model_name = model_name
        self.openai_api_key = openai_api_key
        
        # Initialize LLM
        if openai_api_key:
            self.llm = ChatOpenAI(
                model=model_name,
                api_key=openai_api_key,
                temperature=0.3
            )
        else:
            # Use default configuration - assumes OPENAI_API_KEY is set in environment
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.3
            )
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Initialize agents
        self.agents = self._create_agents()
        
        logging.info(f"Legal Analysis Crew Manager initialized with model: {model_name}")
    
    def _initialize_tools(self) -> Dict[str, Any]:
        """Initialize all available tools"""
        return {
            'context_extraction': LegalContextExtractionTool(),
            'subject_synthesis': SubjectSynthesisTool(),
            'structured_summary': StructuredSummaryTool(),
            'article_analysis': DocumentArticleAnalysisTool(),
            'question_generation': QuestionGenerationTool(),
            'legal_assessment': LegalAssessmentTool(),
            'constitutional_retrieval': ConstitutionalRetrievalTool(),
            'question_answering': QuestionAnsweringTool()
        }
    
    def _create_agents(self) -> Dict[str, Agent]:
        """Create specialized legal analysis agents"""
        
        agents = {}
        
        # Legal Context Analyst Agent
        agents['context_analyst'] = Agent(
            role='Legal Context Analyst',
            goal='Extract comprehensive legal context from documents including entities, actions, and critical points',
            backstory="""You are an expert legal analyst specialized in extracting structured context 
            from legal documents. You excel at identifying key entities, legal actions, deductions, 
            events, and critical attention points that require special consideration.""",
            tools=[self.tools['context_extraction'], self.tools['constitutional_retrieval']],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Subject Matter Expert Agent  
        agents['subject_expert'] = Agent(
            role='Legal Subject Matter Expert',
            goal='Analyze and synthesize the main legal subject and generate structured summaries',
            backstory="""You are a senior legal expert with deep knowledge of various legal domains. 
            You specialize in quickly identifying the core legal subject matter and creating clear, 
            structured summaries that highlight the most important aspects of legal documents.""",
            tools=[self.tools['subject_synthesis'], self.tools['structured_summary']],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Document Structure Analyst Agent
        agents['structure_analyst'] = Agent(
            role='Legal Document Structure Analyst',
            goal='Analyze document structure and break down individual articles with detailed analysis',
            backstory="""You are a legal document specialist who excels at analyzing the structure 
            and organization of legal documents. You can break down complex legal texts into 
            individual articles and provide detailed analysis of each component.""",
            tools=[self.tools['article_analysis']],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Legal Examiner Agent
        agents['legal_examiner'] = Agent(
            role='Legal Examiner and Question Generator',
            goal='Generate relevant legal questions and conduct examinations based on legal content',
            backstory="""You are an experienced legal examiner who creates insightful questions 
            to test understanding of legal documents. You excel at generating both individual 
            questions and comprehensive questionnaires that explore all aspects of legal content.""",
            tools=[self.tools['question_generation'], self.tools['question_answering']],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        
        # Legal Assessment Coordinator Agent (Main Orchestrator)
        agents['assessment_coordinator'] = Agent(
            role='Senior Legal Assessment Coordinator',
            goal='Coordinate comprehensive legal analysis and provide overall assessment with recommendations',
            backstory="""You are a senior legal coordinator with extensive experience in managing 
            complex legal analysis projects. You excel at synthesizing information from multiple 
            specialists and providing comprehensive assessments with practical recommendations.""",
            tools=[self.tools['legal_assessment']],
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )
        
        return agents
    
    def analyze_legal_document(self, document_text: str, document_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform comprehensive legal document analysis using the crew of agents.
        
        Args:
            document_text: The legal document text to analyze
            document_path: Optional path to the document file
            
        Returns:
            Dict containing comprehensive analysis results
        """
        
        try:
            # Create tasks for each agent
            tasks = self._create_analysis_tasks(document_text, document_path)
            
            # Create and execute the crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the analysis
            result = crew.kickoff()
            
            # Process and structure the results
            return self._process_crew_results(result)
            
        except Exception as e:
            logging.error(f"Error in legal document analysis: {e}")
            return {
                "error": f"Failed to analyze document: {str(e)}",
                "success": False
            }
    
    def _create_analysis_tasks(self, document_text: str, document_path: Optional[str] = None) -> List[Task]:
        """Create tasks for the legal analysis crew"""
        
        tasks = []
        
        # Task 1: Legal Context Extraction
        context_task = Task(
            description=f"""
            Extract comprehensive legal context from the provided legal document.
            Document text: {document_text[:2000]}...
            
            Use the legal context extraction tool to identify:
            - Key entities, people, and organizations
            - Legal actions and procedures
            - Important deductions and conclusions
            - Critical events and dates
            - Attention points requiring special consideration
            - Legal terms and penalties
            
            Provide a structured analysis of the legal context.
            """,
            agent=self.agents['context_analyst'],
            expected_output="JSON formatted legal context with categorized information including entities, actions, deductions, events, attention points, legal terms, dates, and penalties."
        )
        tasks.append(context_task)
        
        # Task 2: Subject Synthesis and Structured Summary
        synthesis_task = Task(
            description=f"""
            Analyze the legal document and generate:
            1. A clear synthesis of the main legal subject
            2. A structured summary with organized sections
            
            Document text: {document_text[:2000]}...
            
            Use both subject synthesis and structured summary tools to provide comprehensive analysis.
            The synthesis should capture the essence of the legal matter, and the summary should 
            organize the content into logical, hierarchical sections.
            """,
            agent=self.agents['subject_expert'],
            expected_output="JSON containing both subject synthesis and structured summary with organized sections and subtopics."
        )
        tasks.append(synthesis_task)
        
        # Task 3: Document Structure and Article Analysis
        structure_task = Task(
            description=f"""
            Analyze the structure of the legal document and break it down into individual articles.
            Document text: {document_text[:2000]}...
            Document path: {document_path or 'Not provided'}
            
            Use the article analysis tool to:
            - Identify and separate individual articles
            - Analyze each article for title, category, and summary
            - Determine normative types and components
            - Provide detailed breakdown of document structure
            """,
            agent=self.agents['structure_analyst'],
            expected_output="JSON array with detailed analysis of each article including titles, categories, summaries, and structural components."
        )
        tasks.append(structure_task)
        
        # Task 4: Question Generation and Examination
        examination_task = Task(
            description=f"""
            Generate comprehensive legal questions and examination materials based on the document.
            Document text: {document_text[:2000]}...
            
            Create both:
            1. Individual targeted questions for key aspects
            2. A complete questionnaire with answers for comprehensive evaluation
            
            Focus on creating questions that test understanding of legal concepts, 
            implications, and practical applications.
            """,
            agent=self.agents['legal_examiner'],
            expected_output="JSON containing both individual questions and a complete questionnaire with prompt-completion pairs for legal examination."
        )
        tasks.append(examination_task)
        
        # Task 5: Overall Assessment and Coordination
        assessment_task = Task(
            description=f"""
            Coordinate the comprehensive legal analysis by synthesizing results from all specialists.
            
            Based on the analysis provided by:
            - Legal Context Analyst (entities, actions, critical points)
            - Subject Matter Expert (synthesis and structured summary)  
            - Document Structure Analyst (article breakdown and analysis)
            - Legal Examiner (questions and examination materials)
            
            Provide an overall assessment that includes:
            - Document complexity and structure evaluation
            - Legal relevance and significance assessment
            - Critical points and recommendations
            - Practical implementation considerations
            - Integration of all specialist findings
            
            Use the legal assessment tool with context from other agents' work.
            """,
            agent=self.agents['assessment_coordinator'],
            expected_output="Comprehensive legal assessment integrating all analysis components with professional evaluation, recommendations, and practical considerations.",
            context=tasks  # This task depends on all previous tasks
        )
        tasks.append(assessment_task)
        
        return tasks
    
    def _process_crew_results(self, crew_result) -> Dict[str, Any]:
        """Process and structure the results from the crew execution"""
        
        try:
            # The crew_result should contain the final assessment
            # Parse and structure the comprehensive analysis
            
            result = {
                "success": True,
                "comprehensive_analysis": str(crew_result),
                "analysis_type": "CrewAI Legal Analysis",
                "model_used": self.model_name,
                "agents_involved": list(self.agents.keys()),
                "tools_used": list(self.tools.keys())
            }
            
            # Try to extract structured data if the result is JSON-like
            try:
                if isinstance(crew_result, str) and (crew_result.strip().startswith('{') or crew_result.strip().startswith('[')):
                    parsed_result = json.loads(crew_result)
                    result["structured_analysis"] = parsed_result
            except json.JSONDecodeError:
                # Result is not JSON, keep as string
                pass
            
            return result
            
        except Exception as e:
            logging.error(f"Error processing crew results: {e}")
            return {
                "error": f"Failed to process analysis results: {str(e)}",
                "success": False,
                "raw_result": str(crew_result)
            }
    
    def generate_legal_questions(self, document_text: str, mode: str = "questionnaire") -> Dict[str, Any]:
        """
        Generate legal questions using the legal examiner agent.
        
        Args:
            document_text: Legal document text
            mode: 'question' for single question, 'questionnaire' for complete questionnaire
            
        Returns:
            Dict containing generated questions
        """
        
        try:
            # Create a simple task for question generation
            question_task = Task(
                description=f"""
                Generate legal questions based on the provided document.
                Mode: {mode}
                Document text: {document_text[:1500]}...
                
                {"Create a comprehensive questionnaire with answers" if mode == "questionnaire" else "Generate a targeted legal question"}
                that tests understanding of the legal concepts and implications.
                """,
                agent=self.agents['legal_examiner'],
                expected_output=f"{'Complete questionnaire with questions and answers' if mode == 'questionnaire' else 'Single targeted legal question'} in JSON format."
            )
            
            # Create a simple crew for this task
            crew = Crew(
                agents=[self.agents['legal_examiner']],
                tasks=[question_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            return {
                "success": True,
                "mode": mode,
                "questions": str(result),
                "generated_by": "Legal Examiner Agent"
            }
            
        except Exception as e:
            logging.error(f"Error generating legal questions: {e}")
            return {
                "error": f"Failed to generate questions: {str(e)}",
                "success": False
            }
    
    def answer_legal_question(self, question: str, documents: str, article: str) -> Dict[str, Any]:
        """
        Answer a legal question using provided documents and context.
        
        Args:
            question: The legal question to answer
            documents: Supporting documents for context
            article: Specific article context
            
        Returns:
            Dict containing the answer and analysis
        """
        
        try:
            # Create task for question answering
            answer_task = Task(
                description=f"""
                Answer the legal question based on the provided documents and article context.
                
                Question: {question}
                Supporting Documents: {documents[:1000]}...
                Article Context: {article[:500]}...
                
                Provide a comprehensive, accurate answer based solely on the provided documentation.
                Include reasoning and cite relevant parts of the documentation.
                """,
                agent=self.agents['legal_examiner'],
                expected_output="Comprehensive legal answer with reasoning and citations from provided documentation."
            )
            
            # Create crew for answering
            crew = Crew(
                agents=[self.agents['legal_examiner']],
                tasks=[answer_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            return {
                "success": True,
                "question": question,
                "answer": str(result),
                "answered_by": "Legal Examiner Agent"
            }
            
        except Exception as e:
            logging.error(f"Error answering legal question: {e}")
            return {
                "error": f"Failed to answer question: {str(e)}",
                "success": False
            }


# Convenience function for backward compatibility
def crewai_enhanced_legal_document_analysis(document_text: str, document_path: Optional[str] = None, 
                                           openai_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for performing CrewAI-based legal document analysis.
    
    This function provides the same interface as the original enhanced_legal_document_analysis
    but uses CrewAI agents for the analysis.
    
    Args:
        document_text: Legal document text to analyze
        document_path: Optional path to the document file
        openai_api_key: Optional OpenAI API key
        
    Returns:
        Dict containing comprehensive legal analysis
    """
    
    manager = LegalAnalysisCrewManager(openai_api_key=openai_api_key)
    return manager.analyze_legal_document(document_text, document_path)


def crewai_enhanced_questionnaire(document_text: str, document_path: Optional[str] = None,
                                 openai_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for generating enhanced questionnaires using CrewAI.
    
    Args:
        document_text: Legal document text
        document_path: Optional document path
        openai_api_key: Optional OpenAI API key
        
    Returns:
        Dict containing enhanced questionnaire
    """
    
    manager = LegalAnalysisCrewManager(openai_api_key=openai_api_key)
    return manager.generate_legal_questions(document_text, mode="questionnaire")