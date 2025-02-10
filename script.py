import os
import shlex
import cantools
import math

id_num = set()
code = ""
fun_code = ""
vital_flag = 0
for file_name in os.listdir("dbc_folder"):
    db = cantools.db.load_file(f'dbc_folder/{file_name}', strict=False)
    # 访问DBC中的消息
    for message in db.messages:
        if message.frame_id not in id_num:
            id_num.add(message.frame_id)
            print(vital_flag)
            if vital_flag==0:
                code += f"if(flag == {message.frame_id})\n"
                code += "then\n"

                for signal in message.signals:
                    buf_parm_1 = math.ceil(14 + (signal.start - 7) / 8)
                    # buf_parm_2 = int( ((signal.start - 7) % 8 + signal.length - 1) / 8 + 1 )
                    buf_parm_2 = math.ceil( (signal.length + 7 - signal.start%8)/8 )
                    if signal.unit is not None:
                        code += f"  subtree:add(buffer({buf_parm_1}, {buf_parm_2}),\"{signal.name}: \" .. buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset} .. \"{signal.unit} \" .. \"[\" .. get{signal.name}Name(buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset}) .. \"]\")\n"
                    else:
                        code += f"  subtree:add(buffer({buf_parm_1}, {buf_parm_2}),\"{signal.name}: \" .. buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset} .. \" \" .. \"[\" .. get{signal.name}Name(buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset}) .. \"]\")\n"

                for signal2 in message.signals:
                    fun_code += f"function get{signal2.name}Name(flag)\n"
                    fun_code += f"  name=\"\"\n"
                    if signal2.choices is not None:
                        for num, desc in signal2.choices.items():
                            fun_code += f"  if(flag=={num})\n"
                            fun_code += f"  then\n"
                            fun_code += f"    return \"{desc}\"\n"
                            fun_code += f"  end\n"
                    fun_code += f"  return name\n"
                    fun_code += "end\n"
            elif vital_flag==50:
                code += f"elseif(flag == {message.frame_id})\n"
                code += "then\n"

                for signal in message.signals:
                    buf_parm_1 = math.ceil(14 + (signal.start - 7) / 8)
                    buf_parm_2 = math.ceil( (signal.length + 7 - signal.start%8)/8 )
                    if signal.unit is not None:
                        code += f"  subtree:add(buffer({buf_parm_1}, {buf_parm_2}),\"{signal.name}: \" .. buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset} .. \"{signal.unit} \" .. \"[\" .. get{signal.name}Name(buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset}) .. \"]\")\n"
                    else:
                        code += f"  subtree:add(buffer({buf_parm_1}, {buf_parm_2}),\"{signal.name}: \" .. buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset} .. \" \" .. \"[\" .. get{signal.name}Name(buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset}) .. \"]\")\n"
                code += "end\n"
                code += "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                for signal2 in message.signals:
                    fun_code += f"function get{signal2.name}Name(flag)\n"
                    fun_code += f"  name=\"\"\n"
                    if signal2.choices is not None:
                        for num, desc in signal2.choices.items():
                            fun_code += f"  if(flag=={num})\n"
                            fun_code += f"  then\n"
                            fun_code += f"    return \"{desc}\"\n"
                            fun_code += f"  end\n"
                    fun_code += f"  return name\n"
                    fun_code += "end\n"
            else:
                code += f"elseif(flag == {message.frame_id})\n"
                code += "then\n"

                for signal in message.signals:
                    buf_parm_1 = math.ceil(14 + (signal.start - 7) / 8)
                    buf_parm_2 = math.ceil( (signal.length + 7 - signal.start%8)/8 )
                    if signal.unit is not None:
                        code += f"  subtree:add(buffer({buf_parm_1}, {buf_parm_2}),\"{signal.name}: \" .. buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset} .. \"{signal.unit} \" .. \"[\" .. get{signal.name}Name(buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset}) .. \"]\")\n"
                    else:
                        code += f"  subtree:add(buffer({buf_parm_1}, {buf_parm_2}),\"{signal.name}: \" .. buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset} .. \" \" .. \"[\" .. get{signal.name}Name(buffer({buf_parm_1}, {buf_parm_2}):bitfield(7-({signal.start}%8), {signal.length})*{signal.scale}+{signal.offset}) .. \"]\")\n"

                for signal2 in message.signals:
                    fun_code += f"function get{signal2.name}Name(flag)\n"
                    fun_code += f"  name=\"\"\n"
                    if signal2.choices is not None:
                        for num, desc in signal2.choices.items():
                            fun_code += f"  if(flag=={num})\n"
                            fun_code += f"  then\n"
                            fun_code += f"    return \"{desc}\"\n"
                            fun_code += f"  end\n"
                    fun_code += f"  return name\n"
                    fun_code += "end\n"

            vital_flag += 1
            if vital_flag==51:
                vital_flag = 0

output_file = 'maincode.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(code)
print(f"main代码已生成并保存到 {output_file} 文件中。")

fun_output_file = "funccode.txt"
with open(fun_output_file, 'w', encoding='utf-8') as file:
    file.write(fun_code)
print(f"func代码已生成并保存到 {fun_output_file} 文件中。")
