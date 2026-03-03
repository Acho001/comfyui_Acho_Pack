class Acho_BatchTextAssembler:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # 控制开关：决定最终输出前几个文本
                # 比如你接了6个，但设置 batch_size 为 2，就只输出前两个
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 6, "step": 1}),
            },
            "optional": {
                # 强制要求输入（forceInput），这样它们是连接点而不是文本框
                "text0": ("STRING", {"forceInput": True}),
                "text1": ("STRING", {"forceInput": True}),
                "text2": ("STRING", {"forceInput": True}),
                "text3": ("STRING", {"forceInput": True}),
                "text4": ("STRING", {"forceInput": True}),
                "text5": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("text_batch_list", "actual_count")
    
    # 【核心魔法】OUTPUT_IS_LIST
    # (True, False) 对应上面的 RETURN_TYPES
    # True: 表示 text_batch_list 是一个列表，ComfyUI 会把这个列表里的每一项拆开，
    #       让后面的节点运行 N 次（实现 Batch 效果）。
    # False: 表示 actual_count 只是一个普通数字，不需要拆分。
    OUTPUT_IS_LIST = (True, False)

    FUNCTION = "assemble_batch"
    CATEGORY = "Acho Tools"

    def assemble_batch(self, batch_size, text0=None, text1=None, text2=None, text3=None, text4=None, text5=None):
        # 1. 收集所有输入
        raw_list = [text0, text1, text2, text3, text4, text5]
        
        # 2. 过滤掉没连接的 (None)
        # 这样即使你中间空了一个没接，也不会报错
        valid_list = [t for t in raw_list if t is not None]
        
        # 3. 截取：根据 int 开关 (batch_size) 决定输出多少个
        # 比如 valid_list 有 5 个，batch_size 是 3，则只保留前 3 个
        final_list = valid_list[:batch_size]
        
        # 4. 保护机制：如果列表是空的（没接线），塞一个空字符串防止后续节点崩溃
        if not final_list:
            final_list = [""]
            
        count = len(final_list)

        # 返回注意：
        # 第一个返回值必须是 list，因为 OUTPUT_IS_LIST 设为了 True
        # 第二个返回值是 int
        return (final_list, count)
