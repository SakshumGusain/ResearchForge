from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    gemini_api_key: str
    tavily_api_key: str
    tavily_max_results: int = 5
    
    gemini_model: str
    gemini_embedding_model: str
    
    chroma_persist_dir: str
    chroma_collection_name: str
    
    max_revision_iterations: int = 3
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )
    
settings = Config()