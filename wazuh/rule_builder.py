"""
Wazuh Custom Detection Rule Builder
====================================
Generates production-ready XML rules for Wazuh Manager (/var/ossec/etc/rules/local_rules.xml).
Includes preset rules for Ransomware, Brute-Force, USB Exfiltration, and Suspicious PowerShell.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class CustomRule:
    rule_id: int
    level: int
    description: str
    group: str
    category: str
    match_pattern: str
    decoded_as: str = "syslog"
    mitre_id: str = ""
    frequency: int = 5
    timeframe: int = 60
    active_response: str = ""

    def to_xml(self) -> str:
        """Render the rule object into valid Wazuh XML format."""
        xml_lines = [
            f'  <rule id="{self.rule_id}" level="{self.level}">',
        ]
        if self.group:
            xml_lines.append(f'    <group>{self.group}</group>')
        if self.match_pattern:
            xml_lines.append(f'    <match>{self.match_pattern}</match>')
        if self.mitre_id:
            xml_lines.append(f'    <mitre><id>{self.mitre_id}</id></mitre>')
        xml_lines.append(f'    <description>{self.description}</description>')
        xml_lines.append('  </rule>')
        return "\n".join(xml_lines)


DEFAULT_RULE_PRESETS = [
    CustomRule(
        rule_id=100001,
        level=14,
        description="Ransomware Activity: Rapid file extension modification (.locked, .crypto)",
        group="malware,ransomware",
        category="Ransomware",
        match_pattern="\\.locked|\\.crypto|\\.enc|\\.ransom",
        mitre_id="T1486",
    ),
    CustomRule(
        rule_id=100002,
        level=12,
        description="Suspicious PowerShell Execution with Encoded Command or ExecutionPolicy Bypass",
        group="windows,powershell",
        category="Execution",
        match_pattern="powershell.*-Enc|powershell.*-ExecutionPolicy Bypass",
        mitre_id="T1059.001",
    ),
    CustomRule(
        rule_id=100003,
        level=10,
        description="RDP Brute-Force: Multiple failed Remote Desktop logon attempts",
        group="authentication,brute_force",
        category="Initial Access",
        match_pattern="An account failed to log on.*Logon Type: 10",
        mitre_id="T1110",
        frequency=5,
        timeframe=120,
    ),
    CustomRule(
        rule_id=100004,
        level=11,
        description="Unauthorized USB Storage Device Insertion Detected",
        group="usb,data_exfiltration",
        category="Exfiltration",
        match_pattern="USBSTOR\\\\Disk",
        mitre_id="T1091",
    ),
    CustomRule(
        rule_id=100005,
        level=13,
        description="Privilege Escalation: Unauthorized sudo to ROOT or RunAs Administrator",
        group="privilege_escalation",
        category="Privilege Escalation",
        match_pattern="sudo.*root|runas.*/user:administrator",
        mitre_id="T1078",
    ),
]


def generate_rules_file_xml(rules: List[CustomRule]) -> str:
    """Generate a complete local_rules.xml file content for Wazuh Manager."""
    rules_xml = "\n\n".join(r.to_xml() for r in rules)
    return f"""<!-- Local rules for ShieldEDR Wazuh Integration -->
<group name="local,shield_edr,">
{rules_xml}
</group>
"""
