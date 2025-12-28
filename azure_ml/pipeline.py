"""Azure ML federated learning pipeline."""

from azureml.core import Workspace, Experiment
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import PythonScriptStep
from config.azure_config import azure_config
from config.logging_config import get_logger
from .setup_compute import get_or_create_workspace, setup_compute_cluster
from .components import create_environment

logger = get_logger(__name__)


def create_fl_pipeline(ws: Workspace) -> Pipeline:
    """
    Create federated learning pipeline.
    
    Args:
        ws: Azure ML workspace
        
    Returns:
        Pipeline instance
    """
    # Get compute
    compute_target = setup_compute_cluster(ws)
    
    # Create environment
    env = create_environment()
    
    # Pipeline steps would go here
    # This is a placeholder for the actual FL pipeline
    
    logger.info("Created FL pipeline")
    
    # Return empty pipeline for now
    return None


def run_pipeline(ws: Workspace, pipeline: Pipeline, experiment_name: str = None):
    """
    Run the pipeline.
    
    Args:
        ws: Workspace
        pipeline: Pipeline to run
        experiment_name: Experiment name
    """
    if experiment_name is None:
        experiment_name = azure_config.experiment_name
    
    experiment = Experiment(ws, experiment_name)
    
    logger.info(f"Submitting pipeline to experiment: {experiment_name}")
    
    run = experiment.submit(pipeline)
    
    logger.info(f"Pipeline run submitted: {run.id}")
    
    return run


def main():
    """Main pipeline function."""
    ws = get_or_create_workspace()
    pipeline = create_fl_pipeline(ws)
    
    if pipeline:
        run = run_pipeline(ws, pipeline)
        run.wait_for_completion(show_output=True)


if __name__ == "__main__":
    main()
