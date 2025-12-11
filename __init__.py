from .src.any_switch import AnyInputSwitch
from .src.simple_code import Acho_SimpleCode
from .src.batch_text_assembler import Acho_BatchTextAssembler


NODE_CLASS_MAPPINGS = {
    "Acho_AnyInputSwitch": AnyInputSwitch,
    "Acho_SimpleCode": Acho_SimpleCode,
    "Acho_BatchTextAssembler": Acho_BatchTextAssembler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Acho_AnyInputSwitch": "Acho Switch (0-5)",
    "Acho_SimpleCode": "Acho Simple Code",
    "Acho_BatchTextAssembler": "Acho Batch Text Assembler"
}

ascii_art = """
                                           
   █████╗    ████╗ ██╗   ██╗   █████╗ 
 ██║   ██║ ██╔═══╝ ██║   ██║ ██║   ██║
 ██║   ██║ ██║     ████████║ ██║   ██║
 ████████║ ██╚═══╗ ██║   ██║ ██║   ██║
 ██║   ██║ ██████║ ██║   ██║  ██████║
 ╚═╝   ╚═╝ ╚═════╝ ╚═╝   ╚═╝  ╚═════╝
                                                                       

"""
print(ascii_art)
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
