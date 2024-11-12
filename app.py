import os

from theflow.settings import settings as flowsettings

KH_APP_DATA_DIR = getattr(flowsettings, "KH_APP_DATA_DIR", ".")
GRADIO_TEMP_DIR = os.getenv("GRADIO_TEMP_DIR", None)
# override GRADIO_TEMP_DIR if it's not set
if GRADIO_TEMP_DIR is None:
    GRADIO_TEMP_DIR = os.path.join(KH_APP_DATA_DIR, "gradio_tmp")
    os.environ["GRADIO_TEMP_DIR"] = GRADIO_TEMP_DIR
    
    
## monkey patching default settings
from ktem.index.file.pipelines import DocumentRetrievalPipeline

original_settings = DocumentRetrievalPipeline.get_user_settings

def retrieval_default_settings():
    print("Using custom default settings")
    settings = original_settings()
    settings["use_llm_reranking"] = {
        "name": "Use LLM relevant scoring",
        "value": False,
        "choices": [True, False],
        "component": "checkbox",
    }
    return settings

DocumentRetrievalPipeline.get_user_settings = retrieval_default_settings


from ktem.main import App  # noqa

app = App()
demo = app.make()
demo.queue().launch(
    favicon_path=app._favicon,
    inbrowser=True,
    allowed_paths=[
        "libs/ktem/ktem/assets",
        GRADIO_TEMP_DIR,
    ],
)