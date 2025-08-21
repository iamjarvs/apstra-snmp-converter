"""
Syslog message parser for Apstra SNMP converter.
Parses CEF messages and extracts structured data.
"""
import re
import ast
from typing import Dict, Any, Optional

def parse_syslog_message(msg: str) -> Optional[Dict[str, Any]]:
    # Basic CEF detection
    if 'CEF:' not in msg:
        return None
    try:
        # Extract CEF fields
        cef_match = re.search(r'CEF:0\|Apstra\|AOS\|[^|]+\|(?P<event_id>\d+)\|(?P<event_type>[^|]+)\|(?P<event_severity>\d+)\|msg=(?P<msg>.+)', msg)
        if not cef_match:
            return None
        event_id = cef_match.group('event_id')
        event_type = cef_match.group('event_type')
        event_severity = cef_match.group('event_severity')
        msg_data = cef_match.group('msg')
        # Try to parse msg_data as dict
        try:
            data = ast.literal_eval(msg_data)
        except Exception:
            data = {'raw': msg_data}
        return {
            'event_id': event_id,
            'event_type': event_type,
            'event_severity': event_severity,
            'data': data
        }
    except Exception:
        return None
