# CrewAI Enhanced Pipeline for NLP Legal Document Processing
# Provides advanced workflows and pipeline management using CrewAI

import logging
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
import json

from crewai import Agent, Task, Crew
from crewai.tools import tool

from .crewai_config import CrewAINLPConfig
from .crewai_integration import (
    CrewAINLPAgents, enhanced_sentiment_analysis_tool,
    legal_document_classification_tool, comprehensive_legal_analysis_tool,
    text_preprocessing_tool
)


@dataclass
class PipelineResult:
    """Structured result from pipeline execution"""
    pipeline_id: str
    workflow_type: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    execution_time: float
    status: str
    metadata: Dict[str, Any]
    timestamp: str


@dataclass
class TaskDefinition:
    """Enhanced task definition for pipeline workflows"""
    task_id: str
    description: str
    agent_role: str
    tools: List[str]
    dependencies: List[str]
    expected_output: str
    priority: int = 1
    timeout: int = 300


class CrewAIPipelineManager:
    """Enhanced pipeline manager for complex NLP workflows"""
    
    def __init__(self, config: CrewAINLPConfig = None):
        self.config = config or CrewAINLPConfig()
        self.agents_factory = CrewAINLPAgents()
        self.execution_history: List[PipelineResult] = []
        self.logger = logging.getLogger(__name__)
    
    def create_legal_document_pipeline(self) -> Dict[str, Any]:
        """Create enhanced pipeline for legal document processing"""
        
        # Define pipeline tasks
        tasks = [
            TaskDefinition(
                task_id="preprocessing",
                description="""
                Pré-processar o documento legal para análise:
                1. Verificar a estrutura do documento
                2. Normalizar formatação e encoding
                3. Identificar seções e artigos
                4. Extrair metadados básicos
                5. Preparar texto para análises subsequentes
                """,
                agent_role="text_analyzer",
                tools=["text_preprocessing_tool"],
                dependencies=[],
                expected_output="Documento pré-processado com metadados estruturais",
                priority=1
            ),
            
            TaskDefinition(
                task_id="legal_identification",
                description="""
                Identificar a natureza e características legais do documento:
                1. Determinar se é um documento legal válido
                2. Identificar o tipo de norma (lei, decreto, portaria, etc.)
                3. Verificar a hierarquia normativa
                4. Identificar órgão emissor e jurisdição
                5. Extrair numeração e data de publicação
                """,
                agent_role="legal_classifier",
                tools=["legal_document_classification_tool"],
                dependencies=["preprocessing"],
                expected_output="Identificação completa da natureza legal do documento",
                priority=2
            ),
            
            TaskDefinition(
                task_id="content_classification",
                description="""
                Classificar o conteúdo e estrutura do documento legal:
                1. Classificar por área do direito
                2. Identificar assunto principal
                3. Categorizar tipos de artigos
                4. Determinar intenções legais
                5. Mapear estrutura normativa
                """,
                agent_role="legal_classifier",
                tools=["comprehensive_legal_analysis_tool"],
                dependencies=["legal_identification"],
                expected_output="Classificação abrangente do conteúdo legal",
                priority=2
            ),
            
            TaskDefinition(
                task_id="sentiment_analysis",
                description="""
                Analisar aspectos emocionais e tonais do documento legal:
                1. Analisar tom geral do documento
                2. Identificar linguagem assertiva vs. permissiva
                3. Detectar urgência ou severidade
                4. Avaliar clareza e objetividade
                5. Analisar impacto emocional das disposições
                """,
                agent_role="sentiment_analyst",
                tools=["enhanced_sentiment_analysis_tool"],
                dependencies=["preprocessing"],
                expected_output="Análise detalhada de sentimentos e tom legal",
                priority=3
            ),
            
            TaskDefinition(
                task_id="structural_analysis",
                description="""
                Analisar a estrutura e organização do documento:
                1. Mapear hierarquia de artigos e incisos
                2. Identificar seções e capítulos
                3. Analisar coesão textual
                4. Verificar padrões de redação legal
                5. Avaliar completude estrutural
                """,
                agent_role="text_analyzer",
                tools=["text_preprocessing_tool"],
                dependencies=["content_classification"],
                expected_output="Análise estrutural detalhada do documento",
                priority=3
            ),
            
            TaskDefinition(
                task_id="synthesis",
                description="""
                Sintetizar todas as análises em um relatório executivo:
                1. Consolidar classificações legais
                2. Resumir análises de sentimento
                3. Destacar aspectos estruturais relevantes
                4. Identificar pontos de atenção
                5. Fornecer recomendações de uso
                6. Gerar título sugerido
                """,
                agent_role="legal_researcher",
                tools=["comprehensive_legal_analysis_tool"],
                dependencies=["content_classification", "sentiment_analysis", "structural_analysis"],
                expected_output="Relatório executivo consolidado com insights e recomendações",
                priority=4
            )
        ]
        
        return {
            "pipeline_id": "legal_document_comprehensive",
            "name": "Pipeline Abrangente de Análise Legal",
            "description": "Pipeline completo para análise de documentos legais",
            "tasks": tasks,
            "estimated_duration": 600,  # 10 minutes
            "complexity": "high"
        }
    
    def create_batch_processing_pipeline(self) -> Dict[str, Any]:
        """Create optimized pipeline for batch document processing"""
        
        tasks = [
            TaskDefinition(
                task_id="batch_preprocessing",
                description="""
                Pré-processar múltiplos documentos em lote:
                1. Verificar formatos e encodings
                2. Normalizar estruturas
                3. Identificar tipos de documento
                4. Preparar para processamento paralelo
                """,
                agent_role="text_analyzer",
                tools=["text_preprocessing_tool"],
                dependencies=[],
                expected_output="Documentos preparados para processamento em lote",
                priority=1
            ),
            
            TaskDefinition(
                task_id="parallel_classification",
                description="""
                Classificar documentos em paralelo:
                1. Aplicar classificação por tipo
                2. Categorizar por área legal
                3. Identificar prioridades de processamento
                4. Agrupar documentos similares
                """,
                agent_role="legal_classifier",
                tools=["legal_document_classification_tool", "comprehensive_legal_analysis_tool"],
                dependencies=["batch_preprocessing"],
                expected_output="Classificação organizada de múltiplos documentos",
                priority=2
            ),
            
            TaskDefinition(
                task_id="quality_assessment",
                description="""
                Avaliar qualidade e completude dos documentos:
                1. Verificar integridade dos textos
                2. Identificar documentos incompletos
                3. Avaliar qualidade de OCR (se aplicável)
                4. Marcar documentos para revisão manual
                """,
                agent_role="text_analyzer",
                tools=["text_preprocessing_tool"],
                dependencies=["parallel_classification"],
                expected_output="Relatório de qualidade e recomendações de processamento",
                priority=3
            ),
            
            TaskDefinition(
                task_id="batch_summary",
                description="""
                Gerar resumo executivo do lote processado:
                1. Estatísticas de classificação
                2. Distribuição por tipos e áreas
                3. Identificação de padrões
                4. Recomendações de organização
                """,
                agent_role="legal_researcher",
                tools=["comprehensive_legal_analysis_tool"],
                dependencies=["quality_assessment"],
                expected_output="Relatório executivo do processamento em lote",
                priority=4
            )
        ]
        
        return {
            "pipeline_id": "batch_processing_optimized",
            "name": "Pipeline Otimizado para Processamento em Lote",
            "description": "Pipeline eficiente para processar múltiplos documentos",
            "tasks": tasks,
            "estimated_duration": 300,  # 5 minutes per batch
            "complexity": "medium"
        }
    
    def execute_pipeline(self, pipeline_config: Dict[str, Any], input_data: Dict[str, Any]) -> PipelineResult:
        """Execute a complete pipeline with the given configuration"""
        
        start_time = time.time()
        pipeline_id = pipeline_config["pipeline_id"]
        
        try:
            self.logger.info(f"Iniciando pipeline {pipeline_id}")
            
            # Create agents
            agents = self._create_pipeline_agents(pipeline_config["tasks"])
            
            # Create tasks in dependency order
            tasks = self._create_pipeline_tasks(pipeline_config["tasks"], agents, input_data)
            
            # Create and execute crew
            crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                verbose=True,
                max_execution_time=pipeline_config.get("estimated_duration", 600)
            )
            
            # Execute pipeline
            result = crew.kickoff()
            
            execution_time = time.time() - start_time
            
            # Create pipeline result
            pipeline_result = PipelineResult(
                pipeline_id=pipeline_id,
                workflow_type=pipeline_config["name"],
                input_data=input_data,
                output_data={"crew_result": str(result)},
                execution_time=execution_time,
                status="success",
                metadata={
                    "tasks_executed": len(tasks),
                    "agents_used": len(agents),
                    "complexity": pipeline_config.get("complexity", "medium")
                },
                timestamp=datetime.now().isoformat()
            )
            
            # Store in execution history
            self.execution_history.append(pipeline_result)
            
            self.logger.info(f"Pipeline {pipeline_id} concluído com sucesso em {execution_time:.2f} segundos")
            
            return pipeline_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            error_result = PipelineResult(
                pipeline_id=pipeline_id,
                workflow_type=pipeline_config["name"],
                input_data=input_data,
                output_data={"error": str(e)},
                execution_time=execution_time,
                status="error",
                metadata={"error_type": type(e).__name__},
                timestamp=datetime.now().isoformat()
            )
            
            self.execution_history.append(error_result)
            self.logger.error(f"Erro na execução do pipeline {pipeline_id}: {e}")
            
            return error_result
    
    def _create_pipeline_agents(self, task_definitions: List[TaskDefinition]) -> Dict[str, Agent]:
        """Create agents needed for pipeline tasks"""
        agents = {}
        agent_roles = set(task.agent_role for task in task_definitions)
        
        for role in agent_roles:
            if role == "sentiment_analyst":
                agents[role] = self.agents_factory.create_sentiment_agent()
            elif role == "legal_classifier":
                agents[role] = self.agents_factory.create_legal_classifier_agent()
            elif role == "text_analyzer":
                agents[role] = self.agents_factory.create_text_analyzer_agent()
            elif role == "legal_researcher":
                # Create a specialized legal researcher agent
                agents[role] = Agent(
                    role="Pesquisador Jurídico Especializado",
                    goal="Realizar síntese e pesquisa contextual de documentos legais",
                    backstory="Especialista em pesquisa jurídica e síntese de análises legais complexas",
                    tools=[comprehensive_legal_analysis_tool, text_preprocessing_tool],
                    verbose=True,
                    allow_delegation=False
                )
        
        return agents
    
    def _create_pipeline_tasks(self, task_definitions: List[TaskDefinition], 
                             agents: Dict[str, Agent], input_data: Dict[str, Any]) -> List[Task]:
        """Create CrewAI tasks from task definitions"""
        tasks = []
        task_map = {}
        
        # Sort tasks by priority and dependencies
        sorted_tasks = sorted(task_definitions, key=lambda t: (t.priority, len(t.dependencies)))
        
        for task_def in sorted_tasks:
            # Get context tasks (dependencies)
            context_tasks = [task_map[dep] for dep in task_def.dependencies if dep in task_map]
            
            # Create task description with input data
            description = task_def.description
            if "text" in input_data:
                description += f"\n\nTEXTO/DOCUMENTO: {input_data['text'][:500]}..."
            
            # Create CrewAI task
            task = Task(
                description=description,
                agent=agents[task_def.agent_role],
                expected_output=task_def.expected_output,
                context=context_tasks if context_tasks else None
            )
            
            tasks.append(task)
            task_map[task_def.task_id] = task
        
        return tasks
    
    def get_pipeline_history(self, limit: int = 10) -> List[PipelineResult]:
        """Get recent pipeline execution history"""
        return self.execution_history[-limit:] if limit > 0 else self.execution_history
    
    def get_pipeline_statistics(self) -> Dict[str, Any]:
        """Get statistics about pipeline executions"""
        if not self.execution_history:
            return {"message": "No pipeline executions recorded"}
        
        total_executions = len(self.execution_history)
        successful_executions = sum(1 for r in self.execution_history if r.status == "success")
        average_execution_time = sum(r.execution_time for r in self.execution_history) / total_executions
        
        pipeline_types = {}
        for result in self.execution_history:
            pipeline_type = result.workflow_type
            if pipeline_type not in pipeline_types:
                pipeline_types[pipeline_type] = {"count": 0, "avg_time": 0}
            pipeline_types[pipeline_type]["count"] += 1
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "success_rate": successful_executions / total_executions * 100,
            "average_execution_time": average_execution_time,
            "pipeline_types": pipeline_types
        }


# Main interface functions for enhanced pipelines
def create_pipeline_manager() -> CrewAIPipelineManager:
    """Create a new pipeline manager instance"""
    return CrewAIPipelineManager()


def execute_legal_document_pipeline(text: str, document_metadata: Dict[str, Any] = None) -> PipelineResult:
    """Execute the comprehensive legal document analysis pipeline"""
    manager = create_pipeline_manager()
    pipeline_config = manager.create_legal_document_pipeline()
    
    input_data = {
        "text": text,
        "metadata": document_metadata or {},
        "processing_type": "comprehensive_legal"
    }
    
    return manager.execute_pipeline(pipeline_config, input_data)


def execute_batch_processing_pipeline(documents: List[Dict[str, Any]]) -> PipelineResult:
    """Execute the batch processing pipeline for multiple documents"""
    manager = create_pipeline_manager()
    pipeline_config = manager.create_batch_processing_pipeline()
    
    input_data = {
        "documents": documents,
        "processing_type": "batch_processing",
        "document_count": len(documents)
    }
    
    return manager.execute_pipeline(pipeline_config, input_data)


def get_available_pipelines() -> Dict[str, Dict[str, Any]]:
    """Get information about available pipelines"""
    manager = create_pipeline_manager()
    
    return {
        "legal_document_comprehensive": {
            "config": manager.create_legal_document_pipeline(),
            "description": "Pipeline completo para análise abrangente de documentos legais",
            "use_case": "Análise detalhada de leis, decretos, contratos e outros documentos jurídicos"
        },
        "batch_processing_optimized": {
            "config": manager.create_batch_processing_pipeline(),
            "description": "Pipeline otimizado para processamento em lote",
            "use_case": "Processamento eficiente de múltiplos documentos simultaneamente"
        }
    }