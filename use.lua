-----------------------------------
-- AVTP Dissector
-- Author Happyoung_South_China_University_Of_Technology
-- Date 2023
-----------------------------------

AVTP_Protocol = Proto("Avtp", "Avtp Finder Protocol")     --avtp是协议名，会变成大写。那么avtp的小写默认为过滤器，第二个参数为协议说明，在wireshark查看具体信息时可以看到


message_id = ProtoField.uint8("avtp.message_id", "MessageID as Filter", base.HEX)     --第一个参数为过滤器，第二个参数为显示包信息时的文字
request_id     = ProtoField.uint8("avtp.requestid"     , "requestID"    , base.HEX)    
response_to    = ProtoField.uint8("avtp.responseto"    , "responseTo"   , base.HEX)
opcode         = ProtoField.uint8("avtp.opcode"        , "opCode"       , base.HEX)

AVTP_Protocol.fields = { message_id, request_id, response_to, opcode }

function AVTP_Protocol.dissector(buffer, pinfo, tree)
  length = buffer:len()
  if length == 0 then return end

  pinfo.cols.protocol = "Zhaixiyang"                                              --这个信息是显示在column上的信息


  -- subtree:add(message_id, buffer(12,2))


  --local flag = buffer(12,2):uint()
  --if (flag == 0x433) then
  --subtree:add(request_id,     buffer(14,2))
  --else
  --subtree:add(response_to,    buffer(16,2))
  --subtree:add(opcode,         buffer(18,2))
  --end
  local hex_timestamp = tostring(buffer(2,8))

  local decimal_timestamp = tonumber(hex_timestamp, 16)

-- 将时间戳单位从纳秒转换为秒
local timestamp_in_seconds = decimal_timestamp / 1e9

-- 分离秒和微秒部分
local whole_seconds = math.floor(timestamp_in_seconds)
local microseconds = (decimal_timestamp % 1e9) / 1e3  -- 从纳秒转换为微秒

-- 使用 os.date 格式化秒部分
local datetime = os.date("%Y-%m-%d %H:%M:%S", whole_seconds)

-- 拼接微秒部分
local full_datetime = string.format("%s.%06d", datetime, microseconds)


local subtree = tree:add(AVTP_Protocol, buffer(), "Zhaixiyang's useful data" .. "-------------------------------------" .. "Message_ID:" .. buffer(12,2) .. "  CAN_Chn:" .. buffer(1,1):bitfield(0,8) + 1 .. "   Time:" .. full_datetime)    --这个是显示在包详细信息上得文字

  -- 使用 os.date 格式化时间
  --local datetime = os.date("!%Y-%m-%d %H:%M:%S", timestamp_in_seconds)
  --subtree:add(buffer(2,8),"可读日期和时间 (UTC): " .. hex_timestamp)
  subtree:add(buffer(2,8),"可读日期和时间 (UTC): " .. full_datetime)

  subtree:add(buffer(12,2),"Message_ID: " .. buffer(12,2))
  subtree:add(buffer(1,1),"CAN_Chn: " .. buffer(1,1):bitfield(0,8) + 1)
  --subtree = subtree:add(buffer(2,4),"The next two bytes")
  local flag = buffer(12,2):uint()

elseif(flag == 1263)
then
  subtree:add(buffer(14, 64),"CCU_DTCCode: " .. buffer(14, 64):bitfield(7-(7%8), 512)*1+0 .. " " .. "[" .. getCCU_DTCCodeName(buffer(14, 64):bitfield(7-(7%8), 512)*1+0) .. "]")
elseif(flag == 992)
then
  subtree:add(buffer(17, 1),"BHS_F_SOC: " .. buffer(17, 1):bitfield(7-(31%8), 8)*1+0 .. "% " .. "[" .. getBHS_F_SOCName(buffer(17, 1):bitfield(7-(31%8), 8)*1+0) .. "]")
  subtree:add(buffer(18, 1),"BHS_F_SOH: " .. buffer(18, 1):bitfield(7-(39%8), 8)*1+0 .. "% " .. "[" .. getBHS_F_SOHName(buffer(18, 1):bitfield(7-(39%8), 8)*1+0) .. "]")

end


end


dofile("ZXY_AVTP_Func.lua")

-- local tcp_port = DissectorTable.get("tcp.port")
-- tcp_port:add(37654, AVTP_Protocol)

local tcp_port = DissectorTable.get("acf.msg_type")
tcp_port:add(1,AVTP_Protocol)

--local tcp_port = DissectorTable.get("ieee1722.subtype")
--tcp_port:add(5,AVTP_Protocol)

-- local tcp_port = DissectorTable.get("frame.packet_flags_direction")
-- tcp_port:add(1,AVTP_Protocol)
