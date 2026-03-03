import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Acho_Pack")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 必须定义 WEB_DIRECTORY 才能让 ComfyUI 加载 web 文件夹下的 JS
WEB_DIRECTORY = "./web"

try:
    from .src.any_switch import AnyInputSwitch
    NODE_CLASS_MAPPINGS["Acho_AnyInputSwitch"] = AnyInputSwitch
    NODE_DISPLAY_NAME_MAPPINGS["Acho_AnyInputSwitch"] = "Acho Switch (0-5)"
except Exception as e:
    logger.error(f"Failed to load Acho_AnyInputSwitch: {e}")

try:
    from .src.simple_code import Acho_SimpleCode
    NODE_CLASS_MAPPINGS["Acho_SimpleCode"] = Acho_SimpleCode
    NODE_DISPLAY_NAME_MAPPINGS["Acho_SimpleCode"] = "Acho Simple Code"
except Exception as e:
    logger.error(f"Failed to load Acho_SimpleCode: {e}")

try:
    from .src.batch_text_assembler import Acho_BatchTextAssembler
    NODE_CLASS_MAPPINGS["Acho_BatchTextAssembler"] = Acho_BatchTextAssembler
    NODE_DISPLAY_NAME_MAPPINGS["Acho_BatchTextAssembler"] = "Acho Batch Text Assembler"
except Exception as e:
    logger.error(f"Failed to load Acho_BatchTextAssembler: {e}")

ascii_art = """
                                           
   █████╗    ████╗ ██╗   ██╗   █████╗ 
 ██║   ██║ ██╔═══╝ ██║   ██║ ██║   ██║
 ██║   ██║ ██║     ████████║ ██║   ██║
 ████████║ ██╚═══╗ ██║   ██║ ██║   ██║
 ██║   ██║ ██████║ ██║   ██║  ██████║
 ╚═╝   ╚═╝ ╚═════╝ ╚═╝   ╚═╝  ╚═════╝
                                                                       

"""
print(ascii_art)
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
