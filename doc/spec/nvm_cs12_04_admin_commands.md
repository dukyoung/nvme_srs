NVM Express NVM Command Set Specification, Revision 1.2


64


**4 Admin Commands for the NVM Command Set**

**4.1**

**Admin Command behavior for the NVM Command Set**

The Admin commands are as defined in the NVM Express Base Specification. The NVM Command Set
specific behavior for Admin commands is described in this section.

**Asynchronous Event Request command**
The Asynchronous Event Request command operates as defined in the NVM Express Base Specification.
In addition to the Asynchronous Events defined in the NVM Express Base Specification, the NVM
Command Set defines the Asynchronous Events defined in this section.

**Figure 89: Asynchronous Event Information – Notice**

**Value**

**Definition**

00h

**Attached Namespace Attribute Changed: The Attached Namespace Attribute Changed**
asynchronous event operates as defined in the NVM Express Base Specification with the following
modifications.
A controller shall not send this event if:
a)
the value in the Namespace Utilization field (refer to Figure 114) has changed, as this is a
frequent event that does not require action by the host; or
b)
capacity information (i.e., the NUSE field and the NVMCAP field) returned in the Identify
Namespace data structure (refer to Figure 114) changed as a result of an ANA state change.

05h
LBA Status Information Alert: The criteria for generating an LBA Status Information Alert Notice event
have been met (refer to section 5.2.1). Information about Potentially Unrecoverable LBAs is available
in the LBA Status Information log page (refer to section 4.1.4.5). To clear this event, the host issues a
Get Log Page command with Retain Asynchronous Event bit cleared to ‘0’ for the LBA Status

**Information log page.**

09h

**Allocated Namespace Attribute Changed: The Allocated Namespace Attribute Changed**
asynchronous event operates as defined in the NVM Express Base Specification with the following
modifications.
A controller shall not send this event if:
a)
the value in the Namespace Utilization field (refer to Figure 114) has changed, as this is a
frequent event that does not require action by the host; or
b)
capacity information (i.e., the NUSE field and the NVMCAP field) returned in the Identify
Namespace data structure (refer to Figure 114) changed as a result of an ANA state change.

**Format NVM command**
The Format NVM command operates as defined in the NVM Express Base Specification. The Format Index
indicates a valid LBA Format from the LBA Format field in the Identify Namespace data structure (refer to
section 5.5). Other NVM Command Set specific fields are defined in Figure 90.
For the NVM Command Set, if the Format NVM command results in a change of the logical block size for
the namespace, then the resulting namespace size (i.e., NSZE) (refer to Figure 114) and the namespace
capacity (i.e., NCAP) (refer to Figure 114) may differ from the values indicated prior to the processing of
the Format NVM command.


||Value|||Definition||
|---|---|---|---|---|---|
|00h|||Attached Namespace Attribute Changed: The Attached Namespace Attribute Changed<br>asynchronous event operates as defined in the NVM Express Base Specification with the following<br>modifications.<br>A controller shall not send this event if:<br>a) the value in the Namespace Utilization field (refer to Figure 114) has changed, as this is a<br>frequent event that does not require action by the host; or<br>b) capacity information (i.e., the NUSE field and the NVMCAP field) returned in the Identify<br>Namespace data structure (refer to Figure 114) changed as a result of an ANA state change.|||
|05h|||LBA Status Information Alert: The criteria for generating an LBA Status Information Alert Notice event<br>have been met (refer to section 5.2.1). Information about Potentially Unrecoverable LBAs is available<br>in the LBA Status Information log page (refer to section 4.1.4.5). To clear this event, the host issues a<br>Get Log Page command with Retain Asynchronous Event bit cleared to ‘0’ for the LBA Status<br>Information log page.|||
|09h|||Allocated Namespace Attribute Changed: The Allocated Namespace Attribute Changed<br>asynchronous event operates as defined in the NVM Express Base Specification with the following<br>modifications.<br>A controller shall not send this event if:<br>a) the value in the Namespace Utilization field (refer to Figure 114) has changed, as this is a<br>frequent event that does not require action by the host; or<br>b) capacity information (i.e., the NUSE field and the NVMCAP field) returned in the Identify<br>Namespace data structure (refer to Figure 114) changed as a result of an ANA state change.|||

65
If the LBA Format Extension Enable (LBAFEE) field is not set to 1h in the Host Behavior Support feature
(refer to the Host Behavior Support section in the NVM Express Base Specification), then the controller
aborts a Format NVM command with a status code of Invalid Namespace or Format that specifies an LBA
format (refer to section 5.3.1) of, or specifies an individual namespace formatted with:
a) 16b Guard Protection Information with the STS field set to a non-zero value;
b) 32b Guard Protection Information; or
c) 64b Guard Protection Information.
If:
•
the LBA Format Extension Enable (LBAFEE) field is set to 1h in the Host Behavior Support feature;
•
the Format NVM command specifies an LBA format with the STS field set to a non-zero value; and
•
at least one namespace affected by that command is not formatted with that same LBA format,
then the controller shall abort the command with a status code of Invalid Namespace or Format.
If Flexible Data Placement (refer to the NVM Express Base Specification) is enabled in the Endurance
Group associated with the specified namespace, then:
•
If any Reclaim Unit Handle utilized by the specified namespace is shared by other namespaces
and the specified Format Index does not match the Format Index of the other namespaces, then
the command shall be aborted with a status code of Invalid Format. Refer to section 4.1.6.

**Figure 90: Format NVM – Command Dword 10 – NVM Command Set Specific Fields**

**Bits**

**Description**
Protection Information Location (PIL): If this bit is set to ‘1’ and protection information is enabled (refer
to section 5.3), then protection information is transferred as the first bytes of metadata. If this bit is cleared
to ‘0’ and protection information is enabled, then protection information is transferred as the last bytes of
metadata. This setting is reported in the End-to-end Data Protection Type Settings (DPS) field of the
Identify Namespace data structure and is constrained by the End-to-end Data Protection Capabilities
(DPC) field of the Identify Namespace data structure. For implementations compliant with version 1.0 or
later of the NVM Express NVM Command Set Specification, this bit shall be cleared to ‘0’.

07:05
Protection Information (PI): This field specifies whether end-to-end data protection is to be enabled and
if enabled, the type of protection information to use. The values for this field have the following meanings:

**Value**

**Definition**
000b
Protection information is not enabled
001b
Type 1 protection information is enabled
010b
Type 2 protection information is enabled
011b
Type 3 protection information is enabled
100b to 111b
Reserved
If end-to-end data protected is enabled, the host specifies the appropriate protection information in Copy
commands, Read commands, Verify commands, Write commands, and Compare commands.
Metadata Settings (MSET): This bit is set to ‘1’ if the metadata is transferred as part of an extended data
LBA. This bit is cleared to ‘0’ if the metadata is transferred as part of a separate buffer. The metadata may
include protection information, based on the Protection Information (PI) field. If the Metadata Size for the
LBA Format selected is 0h, then this bit shall be ignored by the controller.

**Get Features & Set Features commands**
Figure 91 defines the Features support requirements for I/O Controllers supporting the NVM Command
Set.


||Bits|||Description||
|---|---|---|---|---|---|
|08|||Protection Information Location (PIL): If this bit is set to ‘1’ and protection information is enabled (refer<br>to section 5.3), then protection information is transferred as the first bytes of metadata. If this bit is cleared<br>to ‘0’ and protection information is enabled, then protection information is transferred as the last bytes of<br>metadata. This setting is reported in the End-to-end Data Protection Type Settings (DPS) field of the<br>Identify Namespace data structure and is constrained by the End-to-end Data Protection Capabilities<br>(DPC) field of the Identify Namespace data structure. For implementations compliant with version 1.0 or<br>later of the NVM Express NVM Command Set Specification, this bit shall be cleared to ‘0’.|||
|07:05|||Protection Information (PI): This field specifies whether end-to-end data protection is to be enabled and<br>if enabled, the type of protection information to use. The values for this field have the following meanings:<br>Value Definition<br>000b Protection information is not enabled<br>001b Type 1 protection information is enabled<br>010b Type 2 protection information is enabled<br>011b Type 3 protection information is enabled<br>100b to 111b Reserved<br>If end-to-end data protected is enabled, the host specifies the appropriate protection information in Copy<br>commands, Read commands, Verify commands, Write commands, and Compare commands.|||
|04|||Metadata Settings (MSET): This bit is set to ‘1’ if the metadata is transferred as part of an extended data<br>LBA. This bit is cleared to ‘0’ if the metadata is transferred as part of a separate buffer. The metadata may<br>include protection information, based on the Protection Information (PI) field. If the Metadata Size for the<br>LBA Format selected is 0h, then this bit shall be ignored by the controller.|||


||Value|||Definition||
|---|---|---|---|---|---|
|000b|||Protection information is not enabled|||
|001b|||Type 1 protection information is enabled|||
|010b|||Type 2 protection information is enabled|||
|011b|||Type 3 protection information is enabled|||
|100b to 111b|||Reserved|||

66

**Figure 91: Feature Identifiers – NVM Command Set**

**Feature**

**Identifier**

**Persistent Across**

**Power Cycle and**

**Reset1**

**Uses**

**Memory**

**Buffer for**

**Attributes**

**Description**

**Scope**

03h
Yes
Yes
LBA Range Type
Namespace
05h
No
No
Error Recovery
Namespace
0Ah
No
No
Write Atomicity Normal
Controller
15h
No
No
LBA Status Information Report Interval
Controller
1Ch
Yes
Yes
Performance Characteristics
NVM subsystem
Namespace
Notes:
1.
This column is only valid if the feature is not saveable (refer to the NVM Express Base Specification). If the
feature is saveable, then this column is not used and any feature may be configured to be saved across power
cycles and reset.

Figure 92 defines the Set Features command specific status values that are specific to the NVM Command
Set specific Feature Identifiers used during Command Completion.

**Figure 92: Set Features – Command Specific Status Values**

**Value**

**Definition**
14h

**Overlapping Range: This error is indicated if the LBA Range Type data structure has overlapping**

**ranges.**

**4.1.3.1**

**LBA Range Type (Feature Identifier 03h)**
This feature indicates the type and attributes of LBA ranges that are part of the specified namespace. If
multiple Set Features commands for this feature are processed, then only information from the most recent
successful command is retained (i.e., subsequent commands replace information provided by previous
commands).
A Set Features command with the Feature Identifier set to 03h and the NSID field set to FFFFFFFFh shall
be aborted with a status of Invalid Field in Command.
The LBA Range Type feature uses Command Dword 11 and specifies the type and attribute information in
the data structure indicated in Figure 95. The data structure is 4,096 bytes in size and shall be physically
contiguous.
If a Get Features command is submitted for this Feature, the attributes specified in Figure 94 are returned
in Dword 0 of the completion queue entry and the LBA Range Type data structure specified in Figure 95 is
returned in the data buffer for that command.

**Figure 93: LBA Range Type – Command Dword 11**

**Bits**

**Description**
31:06
Reserved

05:00

**Number of LBA Ranges (NUM): This field specifies the number of LBA ranges specified in this**
command. This is a 0’s based value. This field is used for the Set Features command only and is ignored

**by the controller for the Get Features command for this Feature.**


|Feature<br>Identifier||Persistent Across|||Uses||Description|Scope|
|---|---|---|---|---|---|---|---|---|
|||Power Cycle and|||Memory||||
|||1<br>Reset|||Buffer for||||
||||||Attributes||||
|03h|Yes|||Yes|||LBA Range Type|Namespace|
|05h|No|||No|||Error Recovery|Namespace|
|0Ah|No|||No|||Write Atomicity Normal|Controller|
|15h|No|||No|||LBA Status Information Report Interval|Controller|
|1Ch|Yes|||Yes|||Performance Characteristics|NVM subsystem|
|||||||||Namespace|
|Notes:<br>1. This column is only valid if the feature is not saveable (refer to the NVM Express Base Specification). If the<br>feature is saveable, then this column is not used and any feature may be configured to be saved across power<br>cycles and reset.|||||||||


||Value|||Definition||
|---|---|---|---|---|---|
|14h|||Overlapping Range: This error is indicated if the LBA Range Type data structure has overlapping<br>ranges.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:06|||Reserved|||
|05:00|||Number of LBA Ranges (NUM): This field specifies the number of LBA ranges specified in this<br>command. This is a 0’s based value. This field is used for the Set Features command only and is ignored<br>by the controller for the Get Features command for this Feature.|||

67

**Figure 94: LBA Range Type – Completion Queue Entry Dword 0**

**Bits**

**Description**
31:06
Reserved
05:00

**Number of LBA Ranges (NUM): This field indicates the number of valid LBA ranges returned in the**

**data buffer for the command (refer to Figure 95). This is a 0’s based value.**

Each entry in the LBA Range Type data structure is defined in Figure 95. The LBA Range feature is a set
of 64 byte entries; the number of entries is indicated as a command parameter, the maximum number of
entries is 64. The controller is not required to perform validation checks on any of the fields in this data
structure. The LBA ranges should not overlap and may be listed in any order (e.g., ordering by LBA is not
required). If the controller checks for LBA range overlap and the controller detects an LBA range overlap,
then the controller shall abort the command with a status code of Overlapping Range.
For a Get Features command, the controller may clear to zero all unused entries in the LBA Range Type
data structure. For a Set Features command, the controller shall ignore all unused entries in the LBA Range
Type data structure.
If the size of the namespace or the LBA format of the namespace changes, then the specified LBA ranges
may not represent the expected locations in the NVM. After such a change, the host should ensure the
intended LBAs are specified.
The default value for this feature shall clear the Number of LBA Ranges field to 0h (i.e., one LBA Range is
present) and initialize the LBA Range Type data structure to contain a single entry with the:
•
Type field cleared to 0h;
•
Attributes field set to 1h;
•
Starting LBA field cleared to 0h;
•
Number of Logical Blocks field set to indicate the number of LBAs in the namespace; and
•
GUID field cleared to 0h, or set to a globally unique identifier.

**Figure 95: LBA Range Type – Data Structure Entry**

**Bytes**

**Description**

**Type (Type): Specifies the Type of the LBA range. The Types are listed below.**

**Value**

**Definition**
0h
General Purpose
1h
Filesystem
2h
RAID
3h
Cache
4h
Page or swap file
5h to 7Fh
Reserved
80h to FFh
Vendor Specific

**Attributes (ATTRB): Specifies attributes of the LBA range. Each bit defines an attribute.**

**Bits**

**Description**
7:2
Reserved

**Hide LBA Range (HLBAR): If this bit is set to ‘1’, then the LBA range should be hidden**
from the OS / EFI / BIOS. If this bit is cleared to ‘0’, then the area should be visible to the
OS / EFI / BIOS.

**LBA Range Overwriteable (LBARO): If this bit is set to ‘1’, then the LBA range may be**
overwritten. If this bit is cleared to ‘0’, then the area should not be overwritten.
15:02
Reserved


||Bits|||Description||
|---|---|---|---|---|---|
|31:06|||Reserved|||
|05:00|||Number of LBA Ranges (NUM): This field indicates the number of valid LBA ranges returned in the<br>data buffer for the command (refer to Figure 95). This is a 0’s based value.|||


||Bytes|||Description||
|---|---|---|---|---|---|
|00|||Type (Type): Specifies the Type of the LBA range. The Types are listed below.<br>Value Definition<br>0h General Purpose<br>1h Filesystem<br>2h RAID<br>3h Cache<br>4h Page or swap file<br>5h to 7Fh Reserved<br>80h to FFh Vendor Specific|||
|01|||Attributes (ATTRB): Specifies attributes of the LBA range. Each bit defines an attribute.<br>Bits Description<br>7:2 Reserved<br>Hide LBA Range (HLBAR): If this bit is set to ‘1’, then the LBA range should be hidden<br>1 from the OS / EFI / BIOS. If this bit is cleared to ‘0’, then the area should be visible to the<br>OS / EFI / BIOS.<br>LBA Range Overwriteable (LBARO): If this bit is set to ‘1’, then the LBA range may be<br>0<br>overwritten. If this bit is cleared to ‘0’, then the area should not be overwritten.|||
|15:02|||Reserved|||


||Value|||Definition||
|---|---|---|---|---|---|
|0h|||General Purpose|||
|1h|||Filesystem|||
|2h|||RAID|||
|3h|||Cache|||
|4h|||Page or swap file|||
|5h to 7Fh|||Reserved|||
|80h to FFh|||Vendor Specific|||


||Bits|||Description||
|---|---|---|---|---|---|
|7:2|||Reserved|||
|1|||Hide LBA Range (HLBAR): If this bit is set to ‘1’, then the LBA range should be hidden<br>from the OS / EFI / BIOS. If this bit is cleared to ‘0’, then the area should be visible to the<br>OS / EFI / BIOS.|||
|0|||LBA Range Overwriteable (LBARO): If this bit is set to ‘1’, then the LBA range may be<br>overwritten. If this bit is cleared to ‘0’, then the area should not be overwritten.|||

68

**Figure 95: LBA Range Type – Data Structure Entry**

**Bytes**

**Description**
23:16
Starting LBA (SLBA): This field specifies the 64-bit logical block address of the first logical block that
is part of this LBA range.
31:24

**Number of Logical Blocks (NLB): This field specifies the number of logical blocks that are part of**
this LBA range. This is a 0’s based value (e.g., the value 0h specifies one block).

47:32

**Unique Identifier (GUID): This field contains a global unique identifier, for use by the host, that**
uniquely specifies the type of this LBA range. Well known Types may be defined and published on

**the NVM Express website.**
63:48
Reserved

**4.1.3.2**

**Error Recovery (Feature Identifier 05h)**
This Feature controls the error recovery attributes for the specified namespace. The attributes are specified
in Command Dword 11.
If a Get Features command is submitted for this Feature, the attributes described in Figure 96 are returned
in Dword 0 of the completion queue entry for that command.

**Figure 96: Error Recovery – Command Dword 11**

**Bits**

**Description**
31:17
Reserved

**Deallocated or Unwritten Logical Block Error Enable (DULBE): If set to '1', then the Deallocated or**
Unwritten Logical Block error is enabled for the specified namespace. If cleared to '0', then the
Deallocated or Unwritten Logical Block error is disabled for the specified namespace. The host shall only
enable this error if the DAE bit in the NSFEAT field is set to ‘1’ in the Identify Namespace data structure.

**The default value for this bit shall be ‘0’. Refer to section 3.3.3.2.1.**

15:00
Time Limited Error Recovery (TLER): Indicates a limited retry timeout value in 100 millisecond units.
This limit applies to I/O commands that support the Limited Retry bit and that are sent to the namespace
for which this Feature has been set. The timeout starts when error recovery actions have started while
processing the command. A value of 0h indicates that there is no timeout.
Note: This mechanism is primarily intended for use by the host that may have alternate means of
recovering the data.

**4.1.3.3**

**Write Atomicity Normal (Feature Identifier 0Ah)**
This Feature configures the controller operation of the AWUN and NAWUN parameters (refer to section
2.1.4.2). The attributes are specified in Command Dword 11.
If a Get Features command is submitted for this Feature, the attributes specified in Figure 97 are returned
in Dword 0 of the completion queue entry for that command.

**Figure 97: Write Atomicity Normal – Command Dword 11**

**Bits**

**Description**
31:01
Reserved

**Disable Normal (DN): If this bit is set to ‘1’, then the host specifies that AWUN and NAWUN are not**
required and that the controller shall only honor AWUPF and NAWUPF. If this bit is cleared to ‘0’, then
AWUN, NAWUN, AWUPF, and NAWUPF shall be honored by the controller.


||Bytes|||Description||
|---|---|---|---|---|---|
|23:16|||Starting LBA (SLBA): This field specifies the 64-bit logical block address of the first logical block that<br>is part of this LBA range.|||
|31:24|||Number of Logical Blocks (NLB): This field specifies the number of logical blocks that are part of<br>this LBA range. This is a 0’s based value (e.g., the value 0h specifies one block).|||
|47:32|||Unique Identifier (GUID): This field contains a global unique identifier, for use by the host, that<br>uniquely specifies the type of this LBA range. Well known Types may be defined and published on<br>the NVM Express website.|||
|63:48|||Reserved|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:17|||Reserved|||
|16|||Deallocated or Unwritten Logical Block Error Enable (DULBE): If set to '1', then the Deallocated or<br>Unwritten Logical Block error is enabled for the specified namespace. If cleared to '0', then the<br>Deallocated or Unwritten Logical Block error is disabled for the specified namespace. The host shall only<br>enable this error if the DAE bit in the NSFEAT field is set to ‘1’ in the Identify Namespace data structure.<br>The default value for this bit shall be ‘0’. Refer to section 3.3.3.2.1.|||
|15:00|||Time Limited Error Recovery (TLER): Indicates a limited retry timeout value in 100 millisecond units.<br>This limit applies to I/O commands that support the Limited Retry bit and that are sent to the namespace<br>for which this Feature has been set. The timeout starts when error recovery actions have started while<br>processing the command. A value of 0h indicates that there is no timeout.<br>Note: This mechanism is primarily intended for use by the host that may have alternate means of<br>recovering the data.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:01|||Reserved|||
|00|||Disable Normal (DN): If this bit is set to ‘1’, then the host specifies that AWUN and NAWUN are not<br>required and that the controller shall only honor AWUPF and NAWUPF. If this bit is cleared to ‘0’, then<br>AWUN, NAWUN, AWUPF, and NAWUPF shall be honored by the controller.|||

69

**4.1.3.4**

**Asynchronous Event Configuration (Feature Identifier 0Bh)**

**Figure 98: Asynchronous Event Configuration – NVM Command Set specific Bit Definitions**

**Bits**

**Description**

**LBA Status Information Notices (LBASIN): This bit determines whether an asynchronous event**
notification is sent to the host for an LBA Status Information Alert event (refer to Figure 89). If this bit is
set to ‘1’, then the LBA Status Information Alert event is sent to the host when this condition occurs. If
this bit is cleared to ‘0’, then the controller shall not send the LBA Status Information Alert event to the
host.

**4.1.3.5**

**LBA Status Information Attributes (Feature Identifier 15h)**
The LBA Status Information Poll Interval (LSIPI) (refer to Figure 99) is the minimum interval that the host
should wait between subsequent reads of the LBA Status Information log page with the Retain
Asynchronous Event bit cleared to ‘0’. The LBA Status Information Poll Interval (LSIPI) is not changeable
by the host.
The LBA Status Information Report Interval (LSIRI) (refer to Figure 99) is the minimum amount of time that
a controller shall delay before sending an LBA Status Information Alert asynchronous event, if LBA Status
Information Notices are enabled. The default value of the LSIRI is equal to LSIPI.
The host may read the LBA Status Information log page as part of LBA Status Information Alert
asynchronous event processing or the host may use a polled method without enabling LBA Status
Information Notices.
The controller reports the value of the LBA Status Information Attributes in Dword 0 of the completion queue
entry when the host issues either a Set Features or Get Features command for this feature. The host
configures the LBA Status Information Report Interval by issuing a Set Features command for this feature
and specifying the value of the LBA Status Information Report Interval in Command Dword 11 (refer to
Figure 99).
The host should not specify a value for the LBA Status Information Report Interval (LSIRI) which is less
than the LBA Status Information Poll Interval (LSIPI) value reported by the controller. If the host specifies a
value the controller does not support, the controller shall return the closest value supported by the controller
in Dword 0 of the completion queue entry for the Set Features command. The accuracy of the interval
measurement on the part of the controller is implementation specific.
The controller shall not send an LBA Status Information asynchronous event unless:
1. there are Tracked LBAs and:
i.
the LBA Status Information Report Interval condition has been exceeded and the LBA
Status Generation Counter has been incremented since the last LBA Status Information
Alert asynchronous event occurred; or
ii. an implementation specific aggregate threshold, if any exists, of Tracked LBAs has been
exceeded;
or
2. a component (e.g., die or channel) failure has occurred that may result in the controller aborting
commands with Unrecovered Read Error status.


||Bits|||Description||
|---|---|---|---|---|---|
|13|||LBA Status Information Notices (LBASIN): This bit determines whether an asynchronous event<br>notification is sent to the host for an LBA Status Information Alert event (refer to Figure 89). If this bit is<br>set to ‘1’, then the LBA Status Information Alert event is sent to the host when this condition occurs. If<br>this bit is cleared to ‘0’, then the controller shall not send the LBA Status Information Alert event to the<br>host.|||

70
When the host issues a Get Log Page command for Log Page Identifier 0Eh with the Retain Asynchronous
Event bit cleared to ‘0’, the LBA Status Information Alert asynchronous event is cleared, if one was
outstanding, and the LBA Status Information Report Interval is restarted by the controller.
LBAs added to the Tracked LBA List or component failures that generate potential LBAs for an Untracked
LBA list may be coalesced into a single LBA Status Information Alert asynchronous event notification.

**Figure 99: LBA Status Information Attributes – Command Dword 11**

**Bits**

**Description**

31:16

**LBA Status Information Poll Interval (LSIPI): The minimum amount of time in 100 millisecond**
increments that the host should wait between subsequent reads of the LBA Status Information log page
with the Retain Asynchronous Event bit cleared to ‘0’.

15:00

**LBA Status Information Report Interval (LSIRI): If LBA Status Information Notices are enabled, the**
value in this field is the minimum amount of time in 100 millisecond increments that a controller shall
delay before sending an LBA Status Information Alert asynchronous event.

**4.1.3.6**

**Host Behavior Support (Feature Identifier 16h)**
The Host Behavior Support feature operates as defined in the NVM Express Base Specification. In addition
to the requirements in the NVM Express Base Specification, this specification provides NVM Command Set
specific definitions.

**Figure 100: Host Behavior Support – Data Structure**

**Bytes**

**Description**
LBA Format Extension Enable (LBAFEE): This field allows the host to specify support for the extended
LBA formats (refer to the ELBAS bit in the Identify Controller data structure in the NVM Express Base
Specification). Refer to section 4.1.3.6.1 for further details. All values other than 0h and 1h are reserved.

**4.1.3.6.1**

**LBA Format Extensions**
The LBA Format Extension Enable (LBAFEE) field in the Host Behavior Support feature (refer to section
4.1.3.6) allows the host to enable support for extended protection information formats (refer to section 5.3.1)
and for LBA Formats with Format Indexes greater than or equal to 16.
If the LBAFEE field is set to 1h and the ELBAS bit (refer to the Identify Controller data structure in the NVM
Express Base Specification) is set to ‘1’, then the controller:
a) shall report a maximum number that is less than or equal to 64 for:
a. the total number of LBA formats supported (refer to section 5.5); and
b. the number of namespace granularity descriptors (refer to Figure 123);
and
b) is enabled to create namespaces with, format namespaces with, and perform I/O commands on
namespaces with extended protection formats that are supported by the controller.
If the LBAFEE field is cleared to 0h, then the controller:
a) shall report a maximum number that is less than or equal to 16 for:
a. the total number of LBA formats supported (refer to section 5.5); and
b. the number of namespace granularity descriptors;


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||LBA Status Information Poll Interval (LSIPI): The minimum amount of time in 100 millisecond<br>increments that the host should wait between subsequent reads of the LBA Status Information log page<br>with the Retain Asynchronous Event bit cleared to ‘0’.|||
|15:00|||LBA Status Information Report Interval (LSIRI): If LBA Status Information Notices are enabled, the<br>value in this field is the minimum amount of time in 100 millisecond increments that a controller shall<br>delay before sending an LBA Status Information Alert asynchronous event.|||


||Bytes|||Description||
|---|---|---|---|---|---|
|02|||LBA Format Extension Enable (LBAFEE): This field allows the host to specify support for the extended<br>LBA formats (refer to the ELBAS bit in the Identify Controller data structure in the NVM Express Base<br>Specification). Refer to section 4.1.3.6.1 for further details. All values other than 0h and 1h are reserved.|||

71
b) shall not create namespaces with, format namespaces with, or perform I/O commands on
namespaces with extended protection information formats that are supported by the controller;
c) shall not format an individually specified namespace (refer to the Format NVM command section
in the NVM Express Base Specification) that is formatted with an extended protection information
format; and
d) shall not format or perform I/O commands on an individually specified namespace that is formatted
with an LBA Format whose Format Index is greater than the reported total number of LBA formats
supported (refer to section 5.5).
Commands that violate these restrictions shall be aborted with a status code of Invalid Namespace or
Format.

**4.1.3.7**

**Performance Characteristics (Feature Identifier 1Ch)**
This Feature is used by the host to set and get Performance Characteristics information.
If a Get Features command for this feature specifying the SEL field set to 011b (i.e., Supported Capabilities)
reports the NS Specific bit:
a) cleared to ‘0’, then the NVM Subsystem Scope bit is set to ‘1’ in the Feature Identifiers Supported
and Effects log page (refer to NVM Express Base Specification); and
b) set to ‘1’, then the Namespace Scope bit is set to ‘1’ in the Feature Identifiers Supported and Effects
log page.

**Figure 101: Performance Characteristics – Command Dword 11**

**Bits**

**Description**
31:09
Reserved

**Revert Vendor Specific Performance Attribute (RVSPA): If this bit is set to ‘1’ in a Set Features**
command, then the saved attribute value of the Vendor Specific Performance Attribute specified by the
Attribute Index field shall be deleted. If this bit is cleared to ‘0’ in a Set Features command, then the
saved attribute value of the Vendor Specific Performance Attribute specified by the Attribute Index field

**shall not be deleted.**

07:00
Attribute Index (ATTRI): This field specifies the Performance Attribute to be transferred between the
host and controller:

**Value**

**Definition**

**Reference**
00h
Standard Performance Attribute 00h
4.1.3.7.1
BFh to 01h
Reserved
C0h
Performance Attribute Identifier List
4.1.3.7.2
FFh to C1h
Vendor Specific Performance Attribute
4.1.3.7.3

If a Set Features command is issued for this Feature and that command completes successfully, then the
attribute specified by the Attribute Index field is transferred from the data buffer for that command.
If a Get Features command is issued for this Feature and that command completes successfully, then the
attribute specified by the Attribute Index field and the Select field is returned in the data buffer for that
command.
If a Get Features command or a Set Features command specifies an Attribute Index field with an
unsupported value, then the controller shall abort that command with a status code of Invalid Field in
Command.
If the Save and Select Feature Support (SSFS) bit is set to ‘1’ in the Optional NVM Command Support
(ONCS) field of the Identify Controller data structure and the value of the MSVSPA field is non-zero, then:


||Bits|||Description||
|---|---|---|---|---|---|
|31:09|||Reserved|||
|08|||Revert Vendor Specific Performance Attribute (RVSPA): If this bit is set to ‘1’ in a Set Features<br>command, then the saved attribute value of the Vendor Specific Performance Attribute specified by the<br>Attribute Index field shall be deleted. If this bit is cleared to ‘0’ in a Set Features command, then the<br>saved attribute value of the Vendor Specific Performance Attribute specified by the Attribute Index field<br>shall not be deleted.|||
|07:00|||Attribute Index (ATTRI): This field specifies the Performance Attribute to be transferred between the<br>host and controller:<br>Value Definition Reference<br>00h Standard Performance Attribute 00h 4.1.3.7.1<br>BFh to 01h Reserved<br>C0h Performance Attribute Identifier List 4.1.3.7.2<br>FFh to C1h Vendor Specific Performance Attribute 4.1.3.7.3|||


||Value|||Definition|||Reference||
|---|---|---|---|---|---|---|---|---|
|00h|||Standard Performance Attribute 00h|||4.1.3.7.1|||
|BFh to 01h|||Reserved||||||
|C0h|||Performance Attribute Identifier List|||4.1.3.7.2|||
|FFh to C1h|||Vendor Specific Performance Attribute|||4.1.3.7.3|||

72
a) the capabilities for this Feature shall report changeable and saveable; and
b) a Set Features command specifying a Vendor Specific Performance shall specify a saved value. If
a Set Features command is issued for this Feature and specifies:
•
an Attribute Index field specifying a Vendor Specific Performance Attribute; and
•
a Saved bit cleared to ‘0’,
then the controller shall abort that command with a status code of Invalid Field in Command.
If a Set Features command specifies the Attribute Index of a Vendor Specific Performance Attribute that
has a saved value and specifies the RVSPA bit set to ‘1’, then:
•
the saved attribute value of that Vendor Specific Performance Attribute is deleted;
•
the contents of the data buffer are not used;
•
the Save bit is ignored by the controller; and
•
if that Vendor Specific Performance Attribute has not been set by an intervening Set Features
command, then a subsequent Get Features command specifying that Vendor Specific Performance
Attribute will return the default value for that Vendor Specific Performance Attribute.
If a Set Features command specifies the Attribute Index of a Vendor Specific Performance Attribute that
does not have a saved value, and specifies the RVSPA bit set to ‘1’, then:
•
the contents of the data buffer are not used;
•
the Save bit is ignored by the controller; and
•
that command returns a status code of Successful Completion.

**4.1.3.7.1**

**Standard Performance Attribute**
The Random 4 KiB Average Read Latency field of the Standard Performance Attribute (refer to Figure 102)
indicates the range corresponding to the value of the measured average latency. Average latency shall be
measured according to the Latency Test section in the Solid State Storage (SSS) Performance Test
Specification (refer to section 1.6). The Latency Test shall be performed using the PTS-C configuration
parameters (WCE and AR=75). The measured latency is measured by the test loop for R/W% = 100/0 and
Block Size = 4 KiB.
That specification describes reporting requirements for the test system used to perform the test. Reporting
that information about the test system is outside the scope of this specification.
The Standard Performance Attribute is not able to be modified by a Set Features command. If a Set
Features command is issued for the Feature and the Attribute Index field specifies the Standard
Performance Attribute, then the controller shall abort that command with a status code of Invalid Field in
Command.
73

**Figure 102: Performance Characteristics – Standard Performance Attribute**

**Bytes**

**Description**
03:00
Reserved

**Random 4 KiB Average Read Latency (R4KARL): This field indicates the time to complete a 4 KiB**
random read. Each value indicates a range of latencies:

**Value**

**Definition**
00h
Not Reported
01h
Greater than or equal to 100 seconds
02h
Greater than or equal to 50 seconds and less than 100 seconds
03h
Greater than or equal to 10 seconds and less than 50 seconds
04h
Greater than or equal to 5 seconds and less than 10 seconds
05h
Greater than or equal to 1 second and less than 5 seconds
06h
Greater than or equal to 500 milliseconds and less than 1 second
07h
Greater than or equal to 100 milliseconds and less than 500 milliseconds
08h
Greater than or equal to 50 milliseconds and less than 100 milliseconds
09h
Greater than or equal to 10 milliseconds and less than 50 milliseconds
0Ah
Greater than or equal to 5 milliseconds and less than 10 milliseconds
0Bh
Greater than or equal to 1 millisecond and less than 5 milliseconds
0Ch
Greater than or equal to 500 microseconds and less than 1 millisecond
0Dh
Greater than or equal to 100 microseconds and less than 500 microseconds
0Eh
Greater than or equal to 50 microseconds and less than 100 microseconds
0Fh
Greater than or equal to 10 microseconds and less than 50 microseconds
10h
Greater than or equal to 5 microseconds and less than 10 microseconds
11h
Greater than or equal to 1 microsecond and less than 5 microseconds
12h
Greater than or equal to 500 nanoseconds and less than 1 microsecond
13h
Greater than or equal to 100 nanoseconds and less than 500 nanoseconds
14h
Greater than or equal to 50 nanoseconds and less than 100 nanoseconds
15h
Greater than or equal to 10 nanoseconds and less than 50 nanoseconds
16h
Greater than or equal to 5 nanoseconds and less than 10 nanoseconds
17h
Greater than or equal to 1 nanosecond and less than 5 nanoseconds
FFh to 18h
Reserved
4095:05

**Reserved**

**4.1.3.7.2**

**Performance Attribute Identifier List**
The Performance Attribute Identifier List contains the Performance Attribute Identifiers of the Vendor
Specific Performance Attributes, as described in Figure 103.


||Bytes|||Description||
|---|---|---|---|---|---|
|03:00|||Reserved|||
|04|||Random 4 KiB Average Read Latency (R4KARL): This field indicates the time to complete a 4 KiB<br>random read. Each value indicates a range of latencies:<br>Value Definition<br>00h Not Reported<br>01h Greater than or equal to 100 seconds<br>02h Greater than or equal to 50 seconds and less than 100 seconds<br>03h Greater than or equal to 10 seconds and less than 50 seconds<br>04h Greater than or equal to 5 seconds and less than 10 seconds<br>05h Greater than or equal to 1 second and less than 5 seconds<br>06h Greater than or equal to 500 milliseconds and less than 1 second<br>07h Greater than or equal to 100 milliseconds and less than 500 milliseconds<br>08h Greater than or equal to 50 milliseconds and less than 100 milliseconds<br>09h Greater than or equal to 10 milliseconds and less than 50 milliseconds<br>0Ah Greater than or equal to 5 milliseconds and less than 10 milliseconds<br>0Bh Greater than or equal to 1 millisecond and less than 5 milliseconds<br>0Ch Greater than or equal to 500 microseconds and less than 1 millisecond<br>0Dh Greater than or equal to 100 microseconds and less than 500 microseconds<br>0Eh Greater than or equal to 50 microseconds and less than 100 microseconds<br>0Fh Greater than or equal to 10 microseconds and less than 50 microseconds<br>10h Greater than or equal to 5 microseconds and less than 10 microseconds<br>11h Greater than or equal to 1 microsecond and less than 5 microseconds<br>12h Greater than or equal to 500 nanoseconds and less than 1 microsecond<br>13h Greater than or equal to 100 nanoseconds and less than 500 nanoseconds<br>14h Greater than or equal to 50 nanoseconds and less than 100 nanoseconds<br>15h Greater than or equal to 10 nanoseconds and less than 50 nanoseconds<br>16h Greater than or equal to 5 nanoseconds and less than 10 nanoseconds<br>17h Greater than or equal to 1 nanosecond and less than 5 nanoseconds<br>FFh to 18h Reserved|||
|4095:05|||Reserved|||


||Value|||Definition||
|---|---|---|---|---|---|
|00h|||Not Reported|||
|01h|||Greater than or equal to 100 seconds|||
|02h|||Greater than or equal to 50 seconds and less than 100 seconds|||
|03h|||Greater than or equal to 10 seconds and less than 50 seconds|||
|04h|||Greater than or equal to 5 seconds and less than 10 seconds|||
|05h|||Greater than or equal to 1 second and less than 5 seconds|||
|06h|||Greater than or equal to 500 milliseconds and less than 1 second|||
|07h|||Greater than or equal to 100 milliseconds and less than 500 milliseconds|||
|08h|||Greater than or equal to 50 milliseconds and less than 100 milliseconds|||
|09h|||Greater than or equal to 10 milliseconds and less than 50 milliseconds|||
|0Ah|||Greater than or equal to 5 milliseconds and less than 10 milliseconds|||
|0Bh|||Greater than or equal to 1 millisecond and less than 5 milliseconds|||
|0Ch|||Greater than or equal to 500 microseconds and less than 1 millisecond|||
|0Dh|||Greater than or equal to 100 microseconds and less than 500 microseconds|||
|0Eh|||Greater than or equal to 50 microseconds and less than 100 microseconds|||
|0Fh|||Greater than or equal to 10 microseconds and less than 50 microseconds|||
|10h|||Greater than or equal to 5 microseconds and less than 10 microseconds|||
|11h|||Greater than or equal to 1 microsecond and less than 5 microseconds|||
|12h|||Greater than or equal to 500 nanoseconds and less than 1 microsecond|||
|13h|||Greater than or equal to 100 nanoseconds and less than 500 nanoseconds|||
|14h|||Greater than or equal to 50 nanoseconds and less than 100 nanoseconds|||
|15h|||Greater than or equal to 10 nanoseconds and less than 50 nanoseconds|||
|16h|||Greater than or equal to 5 nanoseconds and less than 10 nanoseconds|||
|17h|||Greater than or equal to 1 nanosecond and less than 5 nanoseconds|||
|FFh to 18h|||Reserved|||

74

**Figure 103: Performance Characteristics – Performance Attribute Identifier List**

**Bytes**

**Description**

**Bits**

**Description**
7:3
Reserved

2:0

**Attribute Type (ATTRTYP): Each Performance Attribute Identifier in this list is**
the value of the Performance Attribute Identifier field in the Vendor Specific
Performance Attribute reported in response to a Get Features command
specifying a Select field set to the value of this field.
The value of this field shall be equal to the value of the Select field of the Get
Features command which specified this attribute.

**Value**

**Definition**
000b
Current attribute
001b
Default attribute
010b
Saved attribute
All other values
Reserved

**Maximum Saveable Vendor Specific Performance Attributes (MSVSPA): This field indicates the**

**maximum number of Vendor Specific Performance Attributes which are able to be saved.**

**Unused Saveable Vendor Specific Performance Attributes (USVSPA): This field indicates the**
number of saveable Vendor Specific Performance Attributes which have not been saved. This field

**shall be set to a value less than or equal to MSVSPA.**
15:03

**Reserved**

**Performance Attribute Identifier List**
31:16

**Performance Attribute C1h Identifier (PAC1HI): Contains the Performance Attribute Identifier field**
of Vendor Specific Performance Attribute C1h.
47:32

**Performance Attribute C2h Identifier (PAC2HI): Contains the Performance Attribute Identifier field**

**of Vendor Specific Performance Attribute C2h.**
…
1023:1008

**Performance Attribute FFh Identifier (PACFFHI): Contains the Performance Attribute Identifier**

**field of Vendor Specific Performance Attribute FFh.**
4095:1024

**Reserved**

The value of the MSVSPA field indicates the number of Vendor Specific Performance Attributes which may
be saved. The Attribute Indexes of Vendor Specific Performance Attributes which have been saved may
be discontiguous in the range C1h to FFh.
If a Set Features command specifies a Vendor Specific Performance Attribute (i.e., an Attribute Index field
in the range of C1h to FFh) and the value of the USVSPA field is cleared to 0h, then the controller shall
abort that command with a status code of Invalid Field in Command.
The Performance Attribute Identifier List is reported separately for Current, Default, and Saved attributes.

**If the Save and Select Feature Support (SSFS) bit is set to ‘1’ in the Optional NVM Command Support**
(ONCS) field of the Identify Controller data structure, a Get Features command specifies an Attribute Index
field set to C0h, and the Select field is set to:
•
Current (i.e., 000b), then the controller reports a Performance Attribute Identifier List containing the
Performance Attribute Identifier fields of the attributes reported in response to a Get Features
command specifying a Select field set to Current and an Attribute Index set to a value in the range
C1h to FFh;
•
Default (i.e., 001b), then the controller reports a Performance Attribute Identifier List containing the
Performance Attribute Identifier fields of the attributes reported in response to a Get Features


||Bytes|||Description||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|00|||||Bits|||Description||||
|||||7:3|||Reserved|||||
|||||2:0|||Attribute Type (ATTRTYP): Each Performance Attribute Identifier in this list is<br>the value of the Performance Attribute Identifier field in the Vendor Specific<br>Performance Attribute reported in response to a Get Features command<br>specifying a Select field set to the value of this field.<br>The value of this field shall be equal to the value of the Select field of the Get<br>Features command which specified this attribute.<br>Value Definition<br>000b Current attribute<br>001b Default attribute<br>010b Saved attribute<br>All other values Reserved|||||
|01|||Maximum Saveable Vendor Specific Performance Attributes (MSVSPA): This field indicates the<br>maximum number of Vendor Specific Performance Attributes which are able to be saved.|||||||||
|02|||Unused Saveable Vendor Specific Performance Attributes (USVSPA): This field indicates the<br>number of saveable Vendor Specific Performance Attributes which have not been saved. This field<br>shall be set to a value less than or equal to MSVSPA.|||||||||
|15:03|||Reserved|||||||||
||Performance Attribute Identifier List|||||||||||
|31:16|||Performance Attribute C1h Identifier (PAC1HI): Contains the Performance Attribute Identifier field<br>of Vendor Specific Performance Attribute C1h.|||||||||
|47:32|||Performance Attribute C2h Identifier (PAC2HI): Contains the Performance Attribute Identifier field<br>of Vendor Specific Performance Attribute C2h.|||||||||
|…||||||||||||
|1023:1008|||Performance Attribute FFh Identifier (PACFFHI): Contains the Performance Attribute Identifier<br>field of Vendor Specific Performance Attribute FFh.|||||||||
|4095:1024|||Reserved|||||||||


||Value|||Definition||
|---|---|---|---|---|---|
|000b|||Current attribute|||
|001b|||Default attribute|||
|010b|||Saved attribute|||
|All other values|||Reserved|||

75
command specifying a Select field set to Default and an Attribute Index set to a value in the range
C1h to FFh; or
•
Saved (i.e., 010b), then the controller reports a Performance Attribute Identifier List containing the
Performance Attribute Identifier fields of the attributes reported in response to a Get Features
command specifying a Select field set to Saved and an Attribute Index set to a value in the range
C1h to FFh.
The Performance Attribute Identifier List is not able to be modified by a Set Features command specifying
an Attribute Index field set to C0h. If a Set Features command is issued for this feature and specifies an
Attribute Index field set to C0h, then the controller shall abort that command with a status code of Invalid
Field in Command.

**4.1.3.7.3**

**Vendor Specific Performance Attribute**
The Vendor Specific Performance Attribute is described in Figure 104.

**Figure 104: Performance Characteristics – Vendor Specific Performance Attribute**

**Bytes**

**Description**

15:00
Performance Attribute Identifier (PAID): This field contains an identifier describing the contents of the
Vendor Specific field. Unused Vendor Specific Performance Attributes shall clear this field to 0h.
It may be desirable for this field to be universally unique. In that case this field should be compatible with
the 128-bit Universally Unique Identifier (UUID) specified in RFC 4122. Refer to the NVM Express Base
Specification.
29:16

**Reserved**
31:30
Attribute Length (ATTRL): Indicates the number of valid bytes in the Vendor Specific field. The value
shall be in the range 0h to FE0h.
4095:32

**Vendor Specific (VS)**

**Get Log Page command**
The Get Log Page command operates as defined in the NVM Express Base Specification. In addition to
the requirements in the NVM Express Base Specification, mandatory, optional, and prohibited Log Page
Identifiers are defined in Figure 15.
In addition to the log pages described in the NVM Express Base Specification, the NVM Command Set
defines the log pages described in this section. Log page scope is defined in the NVM Express Base
Specification, except as modified by this specification.
The rules for namespace identifier usage are specified in the NVM Express Base Specification.

**Figure 105: Get Log Page – Log Page Identifiers**

**Log Page Identifier**

**CSI1**

**Scope**

**Log Page Name**

**Reference**
01h
N
Controller
Error Information
4.1.4.1
02h
N
Controller /
Namespace
SMART / Health Information
4.1.4.2

06h
N
Controller / Domain /
NVM subsystem
Device Self-test
4.1.4.3
0Dh
N
NVM subsystem
Persistent Event
4.1.4.4


||Bytes|||Description||
|---|---|---|---|---|---|
|15:00|||Performance Attribute Identifier (PAID): This field contains an identifier describing the contents of the<br>Vendor Specific field. Unused Vendor Specific Performance Attributes shall clear this field to 0h.<br>It may be desirable for this field to be universally unique. In that case this field should be compatible with<br>the 128-bit Universally Unique Identifier (UUID) specified in RFC 4122. Refer to the NVM Express Base<br>Specification.|||
|29:16|||Reserved|||
|31:30|||Attribute Length (ATTRL): Indicates the number of valid bytes in the Vendor Specific field. The value<br>shall be in the range 0h to FE0h.|||
|4095:32|||Vendor Specific (VS)|||


||Log Page Identifier|||1<br>CSI|||Scope|||Log Page Name|||Reference||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|01h|||N|||Controller|||Error Information|||4.1.4.1|||
|02h|||N|||Controller /<br>Namespace|||SMART / Health Information|||4.1.4.2|||
|06h|||N|||Controller / Domain /<br>NVM subsystem|||Device Self-test|||4.1.4.3|||
|0Dh|||N|||NVM subsystem|||Persistent Event|||4.1.4.4|||

76

**Figure 105: Get Log Page – Log Page Identifiers**

**Log Page Identifier**

**CSI1**

**Scope**

**Log Page Name**

**Reference**
0Eh
N
Controller
LBA Status Information
4.1.4.5
22h
N
Endurance Group
Flexible Data Placement (FDP)
Statistics
4.1.4.6

23h
N
Endurance Group
Flexible Data Placement (FDP)
Events
4.1.4.7
Notes:
1.
If multiple I/O Command Sets are supported (refer to the NVM Express Base Specification), then the CSI
field is used by the log page: Y = Yes, N = No. If Yes, then refer to the definition of the log page for details
on usage.

**4.1.4.1**

**Error Information (Log Page Identifier 01h)**
The Error Information log page is as defined in the NVM Express Base Specification. Figure 106 describes
the NVM Command Set specific definition of the LBA field.

**Figure 106: Error Information Log Entry Data Structure – User Data**

**Bytes**

**Description**
23:16

**Logical Block Address (LBA): This field indicates the lowest-numbered LBA that experienced an**
error condition, if applicable.

**4.1.4.2**

**SMART / Health Information (02h)**
The SMART / Health Information log page is as defined in the NVM Express Base Specification. For the
Data Units Read and Data Units Written fields, when the logical block size is a value other than 512 bytes,
the controller shall convert the amount of data read to 512 byte units.

**4.1.4.3**

**Device Self-test (Log Page Identifier 06h)**
The Device Self-test log page is as defined in the NVM Express Base Specification. Figure 107 describes
the NVM Command Set specific definition of the Failing LBA field.

**Figure 107: Self-test Results Data Structure**

**Bytes**

**Description**

23:16
Failing LBA (FLBA): This field indicates the LBA of the logical block that caused the test to fail. If the
device encountered more than one failed logical block during the test, then this field only indicates one
of those failed logical blocks. The contents of this field are valid only when the FLBA Valid bit is set to
‘1’.

**4.1.4.4**

**Persistent Event (Log Page Identifier 0Dh)**
The Persistent Event log page is as defined in the NVM Express Base Specification. Figure 108 describes
the NVM Command Set specific definition of the I/O Command Set specific fields within the Change
Namespace Event Data Format (Event Type 06h) (refer to the NVM Express Base Specification).


||Log Page Identifier|||1<br>CSI|||Scope|||Log Page Name|||Reference||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|0Eh|||N|||Controller|||LBA Status Information|||4.1.4.5|||
|22h|||N|||Endurance Group|||Flexible Data Placement (FDP)<br>Statistics|||4.1.4.6|||
|23h|||N|||Endurance Group|||Flexible Data Placement (FDP)<br>Events|||4.1.4.7|||
|Notes:<br>1. If multiple I/O Command Sets are supported (refer to the NVM Express Base Specification), then the CSI<br>field is used by the log page: Y = Yes, N = No. If Yes, then refer to the definition of the log page for details<br>on usage.|||||||||||||||


||Bytes|||Description||
|---|---|---|---|---|---|
|23:16|||Logical Block Address (LBA): This field indicates the lowest-numbered LBA that experienced an<br>error condition, if applicable.|||


||Bytes|||Description||
|---|---|---|---|---|---|
|23:16|||Failing LBA (FLBA): This field indicates the LBA of the logical block that caused the test to fail. If the<br>device encountered more than one failed logical block during the test, then this field only indicates one<br>of those failed logical blocks. The contents of this field are valid only when the FLBA Valid bit is set to<br>‘1’.|||

77

**Figure 108: Change Namespace Event Data Format (Event Type 06h)**

**Bytes**

**Description**

**Formatted LBA Size (FLBAS): For a create operation, contains the FLBAS value from the Host**
Specified Fields in the Namespace Management command (refer to Figure 125). For a delete operation
that specifies a single namespace this field contains the value from the FLBAS field of the Identify
Namespace data structure (refer to Figure 114) for the namespace being deleted. For a delete operation

**that specifies all namespaces this field is reserved.**

**End-to-end Data Protection Type Settings (DPS): For a create operation, contains the DPS value**
from the Host Specified Fields in the Namespace Management command (refer to Figure 125). For a
delete operation that specifies a single namespace this field contains the value from the DPS field of the
Identify Namespace data structure (refer to Figure 114) for the namespace being deleted. For a delete

**operation that specifies all namespaces this field is reserved.**

**4.1.4.5**

**LBA Status Information (Log Page Identifier 0Eh)**
This log page is used to provide information about subsequent actions the host may take to discover which
logical blocks, in namespaces that are attached to the controller, may no longer be recoverable when read.
This log page contains zero or more LBA Status Log Namespace Elements (refer to Figure 110). If the
controller is unaware of any potentially unrecoverable logical blocks in a given namespace attached to the
controller, then this log page does not return an LBA Status Log Namespace Element for that namespace.
This log page shall not return any LBA Status Log Namespace Elements for namespaces which are not
attached to the controller.
Each LBA Status Log Namespace Element contains zero or more LBA Range Descriptors (refer to Figure
111). Each LBA Range Descriptor describes a range of LBAs that have been detected as being potentially
unrecoverable and should be examined by the host using the mechanism specified in the Recommended
Action Type field (refer to Figure 109) in that LBA Status Log Namespace Element in a subsequent Get
LBA Status command.
The host may identify logical blocks that may no longer be recoverable through the subsequent issuing of
one or more Get LBA Status commands (refer to section 4.2.1). Once identified, the host may then recover
the user data from an alternative source and write that data to the original logical block address in the
namespace. If the user data is written successfully, subsequent reads should not cause unrecoverable read
errors (e.g., as a result of the write changing the physical location of the user data).
Upon receiving an LBA Status Information Alert asynchronous event, the host should send one or more
Get Log Page commands for Log Page Identifier 0Eh with the Retain Asynchronous Event bit set to ‘1’ until
the entire log page is read. To clear the event, the host sends a Get Log Page command for Log Page
Identifier 0Eh with the Retain Asynchronous Event bit cleared to ‘0’. The host decides when to send Get
LBA Status commands and when to recover the LBAs identified by the Get LBA Status commands, relative
to when the host clears the event. Section 5.2.1.1 describes example host implementations. Clearing the
event causes the LBA Status Information Report Interval to be restarted and allows the contents of the log
page to be updated.

**Figure 109: LBA Status Information Log Page**

**Bytes**

**Description**
03:00

**LBA Status Log Page Length (LSLPLEN): This field indicates the length in bytes of the LBA Status**
Information log page.


||Bytes|||Description||
|---|---|---|---|---|---|
|32|||Formatted LBA Size (FLBAS): For a create operation, contains the FLBAS value from the Host<br>Specified Fields in the Namespace Management command (refer to Figure 125). For a delete operation<br>that specifies a single namespace this field contains the value from the FLBAS field of the Identify<br>Namespace data structure (refer to Figure 114) for the namespace being deleted. For a delete operation<br>that specifies all namespaces this field is reserved.|||
|33|||End-to-end Data Protection Type Settings (DPS): For a create operation, contains the DPS value<br>from the Host Specified Fields in the Namespace Management command (refer to Figure 125). For a<br>delete operation that specifies a single namespace this field contains the value from the DPS field of the<br>Identify Namespace data structure (refer to Figure 114) for the namespace being deleted. For a delete<br>operation that specifies all namespaces this field is reserved.|||


||Bytes|||Description||
|---|---|---|---|---|---|
|03:00|||LBA Status Log Page Length (LSLPLEN): This field indicates the length in bytes of the LBA Status<br>Information log page.|||

78

**Figure 109: LBA Status Information Log Page**

**Bytes**

**Description**

07:04

**Number of LBA Status Log Namespace Elements (NLSLNE): This field indicates the number of**
LBA Status Log Namespace Elements (refer to Figure 110) contained in this log page. If this field is
cleared to 0h and the Estimate of Unrecoverable Logical Blocks (ESTULB) field contains a non-zero
value, the host should send Get LBA Status commands for the entire LBA range of each namespace
attached to the controller. If both this field and the Estimate of Unrecoverable Logical Blocks (ESTULB)
are cleared to 0h, the host should not send any Get LBA Status commands for any LBA ranges on any
namespaces attached to the controller as there are no known potentially unrecoverable logical blocks

**in any namespace attached to the controller.**

11:08

**Estimate of Unrecoverable Logical Blocks (ESTULB): This field is an estimate of the sum of the**
total number of potentially unrecoverable logical blocks in all of the namespaces identified in the LBA
Status Log Namespace Elements in this log page. A value of 0h in this field is valid. A value of
FFFFFFFFh indicates no information regarding an estimate of the total number of potentially

**unrecoverable logical blocks is available.**
13:12
Reserved

15:14

**LBA Status Generation Counter (LSGC): Contains a value that is incremented each time the LBA**
Status Log contains one or more LBA Range Descriptors which specify any potentially unrecoverable
logical blocks which were not included in any LBA Range Descriptors the last time the host read the
LBA Status Information log. This field is persistent across power on. If the value of this field is FFFFh,
then the field shall be cleared to 0h when incremented (i.e., rolls over to 0h).

n:16

**LBA Status Log Namespace Element List (LBASLNEL): This field contains the list of LBA Status**
Log Namespace Elements that are present in the log page, if any. LBA Status Log Namespace
Elements are of variable length (refer to Figure 110).

**Figure 110: LBA Status Log Namespace Element**

**Bytes**

**Description**

**Header**
03:00

**Namespace Element Identifier (NEID): This field indicates the Namespace Identifier (NSID) of**
the namespace that this LBA Status Log Namespace Element applies to.

07:04

**Number of LBA Range Descriptors (NLRD): This field indicates the number of LBA Range**
Descriptors (refer to Figure 111) returned by the controller in this LBA Status Log Namespace
Element.
A value of FFFFFFFFh indicates that:
a)
no LBA Range Descriptor list is present;
b)
there is no information available regarding the location of known potentially
unrecoverable blocks in the namespace; and
c)

**the host should examine all LBAs in the namespace.**

**Recommended Action Type (RATYPE): This field indicates the value the host should set the**
Action Type (ATYPE) field to in Get LBA Status commands associated with LBA Range

**Descriptors contained in this LBA Status Log Namespace Element.**
15:09
Reserved

**LBA Range Descriptor List**
31:16

**LBA Range Descriptor 0: This field contains the first LBA Range Descriptor in this LBA Status**
Log Namespace Element, if present.
47:32

**LBA Range Descriptor 1: This field contains the second LBA Range Descriptor in this LBA Status**

**Log Namespace Element, if present.**
…
…
(NLRD*16+31):
(NLRD*16+16)

**LBA Range Descriptor N LRD-1: This field contains the last LBA Range Descriptor in this LBA**
Status Log Namespace Element, if present.


||Bytes|||Description||
|---|---|---|---|---|---|
|07:04|||Number of LBA Status Log Namespace Elements (NLSLNE): This field indicates the number of<br>LBA Status Log Namespace Elements (refer to Figure 110) contained in this log page. If this field is<br>cleared to 0h and the Estimate of Unrecoverable Logical Blocks (ESTULB) field contains a non-zero<br>value, the host should send Get LBA Status commands for the entire LBA range of each namespace<br>attached to the controller. If both this field and the Estimate of Unrecoverable Logical Blocks (ESTULB)<br>are cleared to 0h, the host should not send any Get LBA Status commands for any LBA ranges on any<br>namespaces attached to the controller as there are no known potentially unrecoverable logical blocks<br>in any namespace attached to the controller.|||
|11:08|||Estimate of Unrecoverable Logical Blocks (ESTULB): This field is an estimate of the sum of the<br>total number of potentially unrecoverable logical blocks in all of the namespaces identified in the LBA<br>Status Log Namespace Elements in this log page. A value of 0h in this field is valid. A value of<br>FFFFFFFFh indicates no information regarding an estimate of the total number of potentially<br>unrecoverable logical blocks is available.|||
|13:12|||Reserved|||
|15:14|||LBA Status Generation Counter (LSGC): Contains a value that is incremented each time the LBA<br>Status Log contains one or more LBA Range Descriptors which specify any potentially unrecoverable<br>logical blocks which were not included in any LBA Range Descriptors the last time the host read the<br>LBA Status Information log. This field is persistent across power on. If the value of this field is FFFFh,<br>then the field shall be cleared to 0h when incremented (i.e., rolls over to 0h).|||
|n:16|||LBA Status Log Namespace Element List (LBASLNEL): This field contains the list of LBA Status<br>Log Namespace Elements that are present in the log page, if any. LBA Status Log Namespace<br>Elements are of variable length (refer to Figure 110).|||


||Bytes|||Description||
|---|---|---|---|---|---|
||Header|||||
|03:00|||Namespace Element Identifier (NEID): This field indicates the Namespace Identifier (NSID) of<br>the namespace that this LBA Status Log Namespace Element applies to.|||
|07:04|||Number of LBA Range Descriptors (NLRD): This field indicates the number of LBA Range<br>Descriptors (refer to Figure 111) returned by the controller in this LBA Status Log Namespace<br>Element.<br>A value of FFFFFFFFh indicates that:<br>a) no LBA Range Descriptor list is present;<br>b) there is no information available regarding the location of known potentially<br>unrecoverable blocks in the namespace; and<br>c) the host should examine all LBAs in the namespace.|||
|08|||Recommended Action Type (RATYPE): This field indicates the value the host should set the<br>Action Type (ATYPE) field to in Get LBA Status commands associated with LBA Range<br>Descriptors contained in this LBA Status Log Namespace Element.|||
|15:09|||Reserved|||
||LBA Range Descriptor List|||||
|31:16|||LBA Range Descriptor 0: This field contains the first LBA Range Descriptor in this LBA Status<br>Log Namespace Element, if present.|||
|47:32|||LBA Range Descriptor 1: This field contains the second LBA Range Descriptor in this LBA Status<br>Log Namespace Element, if present.|||
|…|||…|||
|(NLRD*16+31):<br>(NLRD*16+16)|||LBA Range Descriptor N LRD-1: This field contains the last LBA Range Descriptor in this LBA<br>Status Log Namespace Element, if present.|||

79

**Figure 111: LBA Range Descriptor**

**Bytes**

**Description**
07:00
Range Starting LBA (RSLBA): This field specifies the 64-bit address of the first logical block of this
LBA Range.

11:08

**Range Number of Logical Blocks (RNLB): This field contains the number of logical blocks in this**
LBA Range. The controller should return the largest possible value in this field. This is a 0’s based

**value.**
15:12
Reserved

For a given LBA Status Log Namespace Element, if the value in the Recommended Action Type (RATYPE)
field is 10h, then the controller shall not report the same LBA Status Log Namespace Element once the
host issues a Get Log Page command for Log Page Identifier 0Eh with the Retain Asynchronous Event bit
cleared to ‘0’ unless an additional component failure has occurred that may have created additional
Untracked LBAs.

**4.1.4.6**

**Flexible Data Placement (FDP) Statistics (Log Page Identifier 22h)**
The Flexible Data Placement Statistics log page is defined in the NVM Express Base Specification. The I/O
commands that are specifically used by the NVM Command Set for the Host Bytes with Metadata Written
(HBMW) field and the Media Bytes with Metadata Written (MBMW) field are the User Data Out Commands,
the Write Zeroes command, and the Write Uncorrectable command.

**4.1.4.7**

**Flexible Data Placement (FDP) Events (Log Page Identifier 23h)**

**4.1.4.7.1**

**Controller Events**


**4.1.4.7.1.1 Media Reallocated (Event Type 0h)**
The Flexible Data Placement Events log page is defined in the NVM Express Base Specification. Figure
112 describes the NVM Command Set specific definition of the Media Reallocated event.

**Figure 112: Media Reallocated - Event Type Specific Data Structure**

**Bytes**

**Description**

**Specific Event Flags (SEF): This field indicates specific attributes of the event.**

**Bits**

**Description**
07:01
Reserved

**LBA Valid (LBAV): If this bit is set to ‘1’, then the LBA field contains a valid value. If this**
bit is cleared to ‘0’, then the LBA field does not contain a valid value.
Reserved

03:02

**Number of LBAs Moved (NLBAM): This field indicates the number of LBAs moved by the controller from**
a Reclaim Unit written by the host. If the PIV bit is set to ‘1’, then the Placement Identifier field indicates the
Reclaim Unit Handle used to initially write the LBAs. A value of 0h in this field indicates that no number is
being reported. A value of FFFFh means that FFFFh or more LBAs were moved by the controller.

11:04
Logical Block Address (LBA): This field indicates one of the LBAs moved by the controller. If the PIV bit
is set to ‘1’, then the Placement Identifier field indicates the Reclaim Unit Handle used to initially write the
LBAs.
If the LBAV bit is cleared to ‘0’, then this field shall be cleared to 0h and the host should ignore this field.
15:12
Reserved


||Bytes|||Description||
|---|---|---|---|---|---|
|07:00|||Range Starting LBA (RSLBA): This field specifies the 64-bit address of the first logical block of this<br>LBA Range.|||
|11:08|||Range Number of Logical Blocks (RNLB): This field contains the number of logical blocks in this<br>LBA Range. The controller should return the largest possible value in this field. This is a 0’s based<br>value.|||
|15:12|||Reserved|||


||Bytes|||Description||
|---|---|---|---|---|---|
|00|||Specific Event Flags (SEF): This field indicates specific attributes of the event.<br>Bits Description<br>07:01 Reserved<br>LBA Valid (LBAV): If this bit is set to ‘1’, then the LBA field contains a valid value. If this<br>00<br>bit is cleared to ‘0’, then the LBA field does not contain a valid value.|||
|01|||Reserved|||
|03:02|||Number of LBAs Moved (NLBAM): This field indicates the number of LBAs moved by the controller from<br>a Reclaim Unit written by the host. If the PIV bit is set to ‘1’, then the Placement Identifier field indicates the<br>Reclaim Unit Handle used to initially write the LBAs. A value of 0h in this field indicates that no number is<br>being reported. A value of FFFFh means that FFFFh or more LBAs were moved by the controller.|||
|11:04|||Logical Block Address (LBA): This field indicates one of the LBAs moved by the controller. If the PIV bit<br>is set to ‘1’, then the Placement Identifier field indicates the Reclaim Unit Handle used to initially write the<br>LBAs.<br>If the LBAV bit is cleared to ‘0’, then this field shall be cleared to 0h and the host should ignore this field.|||
|15:12|||Reserved|||


||Bits|||Description||
|---|---|---|---|---|---|
|07:01|||Reserved|||
|00|||LBA Valid (LBAV): If this bit is set to ‘1’, then the LBA field contains a valid value. If this<br>bit is cleared to ‘0’, then the LBA field does not contain a valid value.|||

80

**Identify Command**
This specification implements the Identify Command and associated Identify data structures defined in the

in this section. The following table lists the Identify data structures that are added or modified by the NVM
Command Set.
Each I/O Command Set is assigned a specific Command Set Identifier (CSI) value by the NVM Express
Base Specification. The NVM Command Set is assigned a CSI value of 00h.

**Figure 113: CNS Values**

**CNS**

**Value**

**O/M1**

**Definition**

**NSID2**

**CNTID3**

**CSI4**

**Reference**

**Section**

**Active Namespace Management**

00h
M
Identify Namespace data structure for the specified
NSID or the namespace capabilities for the NVM
Command Set. 6
Y
N
N
4.1.5.1

01h
M
Identify Controller data structure for the controller
processing the command. 6
N
N
N
4.1.5.2

05h
M 5
Identify I/O Command Set specific Namespace data
structure for the specified NSID for the I/O Command
Set specified in the CSI field. 6
Y
N
Y
4.1.5.3

06h
M
Identify I/O Command Set specific Controller data
structure for the controller processing the command. 6
N
N
Y
4.1.5.4

09h
O
Identify Namespace data structure for the specified
Format Index containing the namespace capabilities
for the NVM Command Set. 6
N
N
Y
4.1.5.5

0Ah
O
I/O Command Set specific Identify Namespace data
structure for the specified Format Index for the I/O
Command Set specified in the CSI field. 6
N
N
Y
4.1.5.6

11h
O 5
Identify Namespace data structure for the specified
allocated NSID.
Y
N
N
4.1.5.7

16h
O
A Namespace Granularity List (refer to Figure 123) is
returned to the host.
N
N
Y
4.1.5.8

1Bh
O 5
I/O Command Set specific Identify Namespace data
structure for the specified allocated NSID.
Y
N
Y
4.1.5.9
Notes:
1.
O/M definition: O = Optional, M = Mandatory.
2.
The NSID field is used: Y = Yes, N = No.
3.
The CDW10.CNTID field is used: Y = Yes, N = No.
4.
The CDW11.CSI field is used: Y = Yes, N = No.
5.
Mandatory for controllers that support the Namespace Management capability (refer to the NVM Express Base
Specification).
6.
Selection of a UUID may be supported. Refer to the Universally Unique Identifiers (UUIDs) for Vendor Specific
Information section in the NVM Express Base Specification.

**4.1.5.1**

**NVM Command Set Identify Namespace Data Structure (CNS 00h)**
If the Namespace Identifier (NSID) field specifies an active NSID, then the NVM Command Set Identify
Namespace data structure (refer to Figure 114) is returned to the host for that specified namespace. If that
value in the NSID field is an inactive NSID, then the controller returns a zero filled data structure. If the
specified namespace is not associated with an I/O Command Set that supports this data structure, then the
controller shall abort the command with a status code of Invalid I/O Command Set.


||CNS|||1<br>O/M||Definition||2<br>NSID|||3<br>CNTID|||4<br>CSI|||Reference||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Value||||||||||||||||Section||
||Active Namespace Management||||||||||||||||||
|00h|||M|||Identify Namespace data structure for the specified<br>NSID or the namespace capabilities for the NVM<br>6<br>Command Set.|Y|||N|||N|||4.1.5.1|||
|01h|||M|||Identify Controller data structure for the controller<br>6<br>processing the command.|N|||N|||N|||4.1.5.2|||
|05h|||5<br>M|||Identify I/O Command Set specific Namespace data<br>structure for the specified NSID for the I/O Command<br>6<br>Set specified in the CSI field.|Y|||N|||Y|||4.1.5.3|||
|06h|||M|||Identify I/O Command Set specific Controller data<br>6<br>structure for the controller processing the command.|N|||N|||Y|||4.1.5.4|||
|09h|||O|||Identify Namespace data structure for the specified<br>Format Index containing the namespace capabilities<br>6<br>for the NVM Command Set.|N|||N|||Y|||4.1.5.5|||
|0Ah|||O|||I/O Command Set specific Identify Namespace data<br>structure for the specified Format Index for the I/O<br>6<br>Command Set specified in the CSI field.|N|||N|||Y|||4.1.5.6|||
|11h|||5<br>O|||Identify Namespace data structure for the specified<br>allocated NSID.|Y|||N|||N|||4.1.5.7|||
|16h|||O|||A Namespace Granularity List (refer to Figure 123) is<br>returned to the host.|N|||N|||Y|||4.1.5.8|||
|1Bh|||5<br>O|||I/O Command Set specific Identify Namespace data<br>structure for the specified allocated NSID.|Y|||N|||Y|||4.1.5.9|||
|Notes:<br>1. O/M definition: O = Optional, M = Mandatory.<br>2. The NSID field is used: Y = Yes, N = No.<br>3. The CDW10.CNTID field is used: Y = Yes, N = No.<br>4. The CDW11.CSI field is used: Y = Yes, N = No.<br>5. Mandatory for controllers that support the Namespace Management capability (refer to the NVM Express Base<br>Specification).<br>6. Selection of a UUID may be supported. Refer to the Universally Unique Identifiers (UUIDs) for Vendor Specific<br>Information section in the NVM Express Base Specification.|||||||||||||||||||

81
The Reported column in Figure 114 specifies fields in the NVM Command Set Identify Namespace data
structure that define namespace capabilities used by a host to format or create a namespace. If the NSID
field is set to FFFFFFFFh, then the controller shall return an NVM Command Set Identify Namespace data
structure that:
•
for fields in Figure 114 that indicate “Yes” in the Reported column, contain a value that is the same
for all namespaces using any of the LBA formats associated with the Number of LBA Formats field
(refer to section 5.5); and
•
for fields in Figure 114 that indicate “No” in the Reported column, contain a value cleared to 0h.
If the controller supports the Namespace Management capability (refer to the Namespace Management
section in the NVM Express Base Specification) and the NSID field is set to FFFFFFFFh, then the controller
shall return an NVM Command Set Identify Namespace data structure. If the controller does not support
the Namespace Management capability and the NSID field is set to FFFFFFFFh, then the controller may
abort the command with a status code of Invalid Namespace or Format.

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

07:00
M

**Namespace Size (NSZE): This field indicates the total size of the namespace in logical**
blocks. A namespace of size n consists of LBA 0 through LBA (n - 1). The number of
logical blocks is based on the formatted logical block size.
Refer to section 2.1.1 for details on the usage of this field.
No

15:08
M

**Namespace Capacity (NCAP): This field indicates the maximum number of logical**
blocks that may be allocated in the namespace at any point in time. The number of
logical blocks is based on the formatted logical block size. Spare LBAs are not reported
as part of this field.

**Refer to section 2.1.1 for details on the usage of this field.**
No

23:16
M

**Namespace Utilization (NUSE): This field indicates the current number of logical**
blocks allocated in the namespace. This field is less than or equal to the value of the
Namespace Capacity field. The number of logical blocks is based on the formatted
logical block size.
Refer to section 2.1.1 for details on the usage of this field.
No


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|07:00|||M|||Namespace Size (NSZE): This field indicates the total size of the namespace in logical<br>blocks. A namespace of size n consists of LBA 0 through LBA (n - 1). The number of<br>logical blocks is based on the formatted logical block size.<br>Refer to section 2.1.1 for details on the usage of this field.|||No|||
|15:08|||M|||Namespace Capacity (NCAP): This field indicates the maximum number of logical<br>blocks that may be allocated in the namespace at any point in time. The number of<br>logical blocks is based on the formatted logical block size. Spare LBAs are not reported<br>as part of this field.<br>Refer to section 2.1.1 for details on the usage of this field.|||No|||
|23:16|||M|||Namespace Utilization (NUSE): This field indicates the current number of logical<br>blocks allocated in the namespace. This field is less than or equal to the value of the<br>Namespace Capacity field. The number of logical blocks is based on the formatted<br>logical block size.<br>Refer to section 2.1.1 for details on the usage of this field.|||No|||

82

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

M

**Namespace Features (NSFEAT): This field defines features of the namespace.**

**Bits**

**Description**

**Optional Read Performance (OPTRPERF): If this bit is set to ‘1’ then the**
NPRG, BPRA, and NORS fields are defined for this namespace and should
be used by the host for I/O optimization. If this bit is cleared to ‘0’, then the
controller does not support the NPRG, NPRA, and NORS fields for this
namespace.

**Multiple Atomicity Mode (MAM): If this bit is set to ‘1’, then Multiple**
Atomicity Mode (refer to section 2.1.4.5) applies to write operations to this
namespace. If this bit is cleared to ‘0’, then Single Atomicity Mode (refer to

**section 2.1.4.1) applies to write operations to this namespace.**
05:04

**Optional Write Performance (OPTPERF): Indicate support of alignment**
and granularity attributes of this namespace, as described in Figure 115.

**UID Reuse (UIDREUSE): This bit is as defined in the UIDREUSE bit in the**
I/O Command Set Independent Identify Namespace data structure (refer to
the I/O Command Set Independent Identify Namespace data structure

**section in the NVM Express Base Specification).**

**Deallocated Error (DAE): If this bit is set to ‘1’, then the controller supports**
the Deallocated or Unwritten Logical Block error for this namespace. If this
bit is cleared to ‘0’, then the controller does not support the Deallocated or
Unwritten Logical Block error for this namespace. Refer to section

**3.3.3.2.1.**

**Namespace Supported Atomic Boundary & Power (NSABP): If this bit**
is set to ‘1’, then the fields NAWUN, NAWUPF, and NACWU are defined
for this namespace and should be used by the host for this namespace
instead of the AWUN, AWUPF, and ACWU fields in the Identify Controller
data structure. If this bit is cleared to ‘0’, then the controller does not support
the fields NAWUN, NAWUPF, and NACWU for this namespace. In this
case, the host should use the AWUN, AWUPF, and ACWU fields defined
in the Identify Controller data structure in the NVM Express Base

**Specification. Refer to section 2.1.4.**

**Thin Provisioning (THINP): If this bit is set to ‘1’, then the namespace**
supports thin provisioning. If this bit is cleared to ‘0’, then thin provisioning

**is not supported Refer to section 2.1.1 for details on the usage of this bit.**
No

M

**Number of LBA Formats (NLBAF): This field defines the number of supported LBA**
data size and metadata size combinations supported by the namespaces that share the
same set of host-selectable attributes. LBA formats shall be packed sequentially
starting at the LBA Format 0 Support (LBAF0) field. This is a 0’s based value.
Refer to section 5.5 for the structure of the LBA formats, the association to the NULBAF
field, and the maximum values of this field.
The supported LBA formats are indicated in bytes 128 to 383 in this data structure. The
LBA Format fields with a Format Index greater than the value defined by section 5.5 are
invalid and not supported.
The metadata may be either transferred as part of the logical block or may be
transferred as a separate contiguous buffer of data. The metadata shall not be split
between the logical block and a separate metadata buffer. Refer to section 2.1.6.
It is recommended that hosts and controllers transition to an logical block size that is
4 KiB or larger for ECC efficiency at the controller. If providing metadata, it is
recommended that at least 8 bytes are provided per logical block to enable use with
end-to-end data protection, refer to section 5.2.3.
Yes


||Bytes|||1<br>O/M|||Description||||||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|24|||M|||Namespace Features (NSFEAT): This field defines features of the namespace.<br>Bits Description<br>Optional Read Performance (OPTRPERF): If this bit is set to ‘1’ then the<br>NPRG, BPRA, and NORS fields are defined for this namespace and should<br>07 be used by the host for I/O optimization. If this bit is cleared to ‘0’, then the<br>controller does not support the NPRG, NPRA, and NORS fields for this<br>namespace.<br>Multiple Atomicity Mode (MAM): If this bit is set to ‘1’, then Multiple<br>Atomicity Mode (refer to section 2.1.4.5) applies to write operations to this<br>06<br>namespace. If this bit is cleared to ‘0’, then Single Atomicity Mode (refer to<br>section 2.1.4.1) applies to write operations to this namespace.<br>Optional Write Performance (OPTPERF): Indicate support of alignment<br>05:04<br>and granularity attributes of this namespace, as described in Figure 115.<br>UID Reuse (UIDREUSE): This bit is as defined in the UIDREUSE bit in the<br>I/O Command Set Independent Identify Namespace data structure (refer to<br>03<br>the I/O Command Set Independent Identify Namespace data structure<br>section in the NVM Express Base Specification).<br>Deallocated Error (DAE): If this bit is set to ‘1’, then the controller supports<br>the Deallocated or Unwritten Logical Block error for this namespace. If this<br>02 bit is cleared to ‘0’, then the controller does not support the Deallocated or<br>Unwritten Logical Block error for this namespace. Refer to section<br>3.3.3.2.1.<br>Namespace Supported Atomic Boundary & Power (NSABP): If this bit<br>is set to ‘1’, then the fields NAWUN, NAWUPF, and NACWU are defined<br>for this namespace and should be used by the host for this namespace<br>instead of the AWUN, AWUPF, and ACWU fields in the Identify Controller<br>01 data structure. If this bit is cleared to ‘0’, then the controller does not support<br>the fields NAWUN, NAWUPF, and NACWU for this namespace. In this<br>case, the host should use the AWUN, AWUPF, and ACWU fields defined<br>in the Identify Controller data structure in the NVM Express Base<br>Specification. Refer to section 2.1.4.<br>Thin Provisioning (THINP): If this bit is set to ‘1’, then the namespace<br>00 supports thin provisioning. If this bit is cleared to ‘0’, then thin provisioning<br>is not supported Refer to section 2.1.1 for details on the usage of this bit.||||||No|||
|||||||||Bits|||Description||||
||||||||07|||Optional Read Performance (OPTRPERF): If this bit is set to ‘1’ then the<br>NPRG, BPRA, and NORS fields are defined for this namespace and should<br>be used by the host for I/O optimization. If this bit is cleared to ‘0’, then the<br>controller does not support the NPRG, NPRA, and NORS fields for this<br>namespace.|||||
||||||||06|||Multiple Atomicity Mode (MAM): If this bit is set to ‘1’, then Multiple<br>Atomicity Mode (refer to section 2.1.4.5) applies to write operations to this<br>namespace. If this bit is cleared to ‘0’, then Single Atomicity Mode (refer to<br>section 2.1.4.1) applies to write operations to this namespace.|||||
||||||||05:04|||Optional Write Performance (OPTPERF): Indicate support of alignment<br>and granularity attributes of this namespace, as described in Figure 115.|||||
||||||||03|||UID Reuse (UIDREUSE): This bit is as defined in the UIDREUSE bit in the<br>I/O Command Set Independent Identify Namespace data structure (refer to<br>the I/O Command Set Independent Identify Namespace data structure<br>section in the NVM Express Base Specification).|||||
||||||||02|||Deallocated Error (DAE): If this bit is set to ‘1’, then the controller supports<br>the Deallocated or Unwritten Logical Block error for this namespace. If this<br>bit is cleared to ‘0’, then the controller does not support the Deallocated or<br>Unwritten Logical Block error for this namespace. Refer to section<br>3.3.3.2.1.|||||
||||||||01|||Namespace Supported Atomic Boundary & Power (NSABP): If this bit<br>is set to ‘1’, then the fields NAWUN, NAWUPF, and NACWU are defined<br>for this namespace and should be used by the host for this namespace<br>instead of the AWUN, AWUPF, and ACWU fields in the Identify Controller<br>data structure. If this bit is cleared to ‘0’, then the controller does not support<br>the fields NAWUN, NAWUPF, and NACWU for this namespace. In this<br>case, the host should use the AWUN, AWUPF, and ACWU fields defined<br>in the Identify Controller data structure in the NVM Express Base<br>Specification. Refer to section 2.1.4.|||||
||||||||00|||Thin Provisioning (THINP): If this bit is set to ‘1’, then the namespace<br>supports thin provisioning. If this bit is cleared to ‘0’, then thin provisioning<br>is not supported Refer to section 2.1.1 for details on the usage of this bit.|||||
|25|||M|||Number of LBA Formats (NLBAF): This field defines the number of supported LBA<br>data size and metadata size combinations supported by the namespaces that share the<br>same set of host-selectable attributes. LBA formats shall be packed sequentially<br>starting at the LBA Format 0 Support (LBAF0) field. This is a 0’s based value.<br>Refer to section 5.5 for the structure of the LBA formats, the association to the NULBAF<br>field, and the maximum values of this field.<br>The supported LBA formats are indicated in bytes 128 to 383 in this data structure. The<br>LBA Format fields with a Format Index greater than the value defined by section 5.5 are<br>invalid and not supported.<br>The metadata may be either transferred as part of the logical block or may be<br>transferred as a separate contiguous buffer of data. The metadata shall not be split<br>between the logical block and a separate metadata buffer. Refer to section 2.1.6.<br>It is recommended that hosts and controllers transition to an logical block size that is<br>4 KiB or larger for ECC efficiency at the controller. If providing metadata, it is<br>recommended that at least 8 bytes are provided per logical block to enable use with<br>end-to-end data protection, refer to section 5.2.3.||||||Yes|||

83

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

M

**Formatted LBA Size (FLBAS): This field indicates the LBA data size and metadata**
size combination that the namespace has been formatted with (refer to section 4.1.2).

**Bits**

**Description**
Reserved

6:5

**Format Index Upper (FIDXU): This field indicates the most-significant 2**
bits of the Format Index that was used to format the namespace. If the total
number of LBA formats supported (refer to section 5.5) is less than or equal
to 16, then the host should ignore this field.

**Metadata Transferred as Extended LBA (MTELBA): If this bit is set to ‘1’,**

**then metadata is transferred at the end of the logical block, creating an**
extended logical block. If this bit is cleared to ‘0’, then indicates that all of
the metadata for a command is transferred as a separate contiguous buffer
of data. This bit is not applicable when there is no metadata.
3:0

**Format Index Lower (FIDXL): This field indicates the least-significant 4**
bits of the Format Index that was used to format the namespace.
No

M

**Metadata Capabilities (MC): This field indicates the capabilities for metadata.**

**Bits**

**Description**
7:2
Reserved

**Metadata Transferred as Separate Buffer Support (MTSBS): If this bit is**

**set to ‘1’, then the namespace supports the metadata being transferred as**
part of a separate buffer that is specified in the Metadata Pointer. If this bit
is cleared to ‘0’, then the namespace does not support the metadata being
transferred as part of a separate buffer.

**Metadata Transferred as Extended LBA Support (MTELBAS): If this bit**

**is set to ‘1’, then the namespace supports the metadata being transferred**
as part of an extended data LBA. If this bit is cleared to ‘0’, then the
namespace does not support the metadata being transferred as part of an
extended data LBA.
Yes


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|26|||M|||Formatted LBA Size (FLBAS): This field indicates the LBA data size and metadata<br>size combination that the namespace has been formatted with (refer to section 4.1.2).<br>Bits Description<br>7 Reserved<br>Format Index Upper (FIDXU): This field indicates the most-significant 2<br>bits of the Format Index that was used to format the namespace. If the total<br>6:5<br>number of LBA formats supported (refer to section 5.5) is less than or equal<br>to 16, then the host should ignore this field.<br>Metadata Transferred as Extended LBA (MTELBA): If this bit is set to ‘1’,<br>then metadata is transferred at the end of the logical block, creating an<br>4 extended logical block. If this bit is cleared to ‘0’, then indicates that all of<br>the metadata for a command is transferred as a separate contiguous buffer<br>of data. This bit is not applicable when there is no metadata.<br>Format Index Lower (FIDXL): This field indicates the least-significant 4<br>3:0<br>bits of the Format Index that was used to format the namespace.|||No|||
|27|||M|||Metadata Capabilities (MC): This field indicates the capabilities for metadata.<br>Bits Description<br>7:2 Reserved<br>Metadata Transferred as Separate Buffer Support (MTSBS): If this bit is<br>set to ‘1’, then the namespace supports the metadata being transferred as<br>1 part of a separate buffer that is specified in the Metadata Pointer. If this bit<br>is cleared to ‘0’, then the namespace does not support the metadata being<br>transferred as part of a separate buffer.<br>Metadata Transferred as Extended LBA Support (MTELBAS): If this bit<br>is set to ‘1’, then the namespace supports the metadata being transferred<br>0 as part of an extended data LBA. If this bit is cleared to ‘0’, then the<br>namespace does not support the metadata being transferred as part of an<br>extended data LBA.|||Yes|||


||Bits|||Description||
|---|---|---|---|---|---|
|7|||Reserved|||
|6:5|||Format Index Upper (FIDXU): This field indicates the most-significant 2<br>bits of the Format Index that was used to format the namespace. If the total<br>number of LBA formats supported (refer to section 5.5) is less than or equal<br>to 16, then the host should ignore this field.|||
|4|||Metadata Transferred as Extended LBA (MTELBA): If this bit is set to ‘1’,<br>then metadata is transferred at the end of the logical block, creating an<br>extended logical block. If this bit is cleared to ‘0’, then indicates that all of<br>the metadata for a command is transferred as a separate contiguous buffer<br>of data. This bit is not applicable when there is no metadata.|||
|3:0|||Format Index Lower (FIDXL): This field indicates the least-significant 4<br>bits of the Format Index that was used to format the namespace.|||


||Bits|||Description||
|---|---|---|---|---|---|
|7:2|||Reserved|||
|1|||Metadata Transferred as Separate Buffer Support (MTSBS): If this bit is<br>set to ‘1’, then the namespace supports the metadata being transferred as<br>part of a separate buffer that is specified in the Metadata Pointer. If this bit<br>is cleared to ‘0’, then the namespace does not support the metadata being<br>transferred as part of a separate buffer.|||
|0|||Metadata Transferred as Extended LBA Support (MTELBAS): If this bit<br>is set to ‘1’, then the namespace supports the metadata being transferred<br>as part of an extended data LBA. If this bit is cleared to ‘0’, then the<br>namespace does not support the metadata being transferred as part of an<br>extended data LBA.|||

84

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

M

**End-to-end Data Protection Capabilities (DPC): This field indicates the capabilities**
for the end-to-end data protection feature. Multiple bits may be set in this field. Refer to
section 5.3.

**Bits**

**Description**
7:5
Reserved

**Protection Information In Last Bytes (PIILB): If this bit is set to ‘1’, then the**
namespace supports protection information transferred as the last bytes of
metadata. If this bit is cleared to ‘0’, then the namespace does not support
protection information transferred as the last bytes of metadata.

**Protection Information In First Bytes (PIIFB): If this bit is set to ‘1’, then the**
namespace supports protection information transferred as the first bytes of
metadata. If this bit is cleared to ‘0’, then the namespace does not support
protection information transferred as the first bytes of metadata. For
implementations compliant with revision 1.0 or later of the NVM Express NVM
Command Set Specification, this bit shall be cleared to ‘0’.

**Protection Information Type 3 Supported (PIT3S): If this bit is set to ‘1’,**
then the namespace supports Protection Information Type 3. If this bit is
cleared to ‘0’, then the namespace does not support Protection Information
Type 3.

**Protection Information Type 2 Supported (PIT2S): If this bit is set to ‘1’,**
then the namespace supports Protection Information Type 2. If cleared to ‘0’
indicates that the namespace does not support Protection Information Type
2.

**Protection Information Type 1 Supported (PIT1S): If this bit is set to ‘1’,**
then the namespace supports Protection Information Type 1. If this bit is
cleared to ‘0’, then the namespace does not support Protection Information
Type 1.
Yes

M

**End-to-end Data Protection Type Settings (DPS): This field indicates the protection**
information Type settings for the end-to-end data protection feature. Refer to section
5.3.

**Bits**

**Description**
7:4
Reserved

**Protection Information Position (PIP): If this bit is set to ‘1’, then the**
protection information, if enabled, is transferred as the first bytes of
metadata. If this bit is cleared to ‘0’, then the protection information, if
enabled, is transferred as the last bytes of metadata. For implementations
compliant with version 1.0 or later of the NVM Express NVM Command
Set Specification, this bit shall be cleared to ‘0’.

2:0

**Protection Information Type (PIT): This field indicates whether**
protection information is enabled and the type of protection information
enabled. The values for this field have the following meanings:

**Value**

**Definition**
000b
Protection information is not enabled
001b
Type 1 protection information is enabled
010b
Type 2 protection information is enabled
011b
Type 3 protection information is enabled
100b to 111b
Reserved
No

O

**Namespace Multi-path I/O and Namespace Sharing Capabilities (NMIC): This field**
is as defined in the I/O Command Set Independent Identify Namespace data structure
(refer to the I/O Command Set Independent Identify Namespace data structure section
in the NVM Express Base Specification).
Yes


||Bytes|||1<br>O/M|||Description|||||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|28|||M|||End-to-end Data Protection Capabilities (DPC): This field indicates the capabilities<br>for the end-to-end data protection feature. Multiple bits may be set in this field. Refer to<br>section 5.3.<br>Bits Description<br>7:5 Reserved<br>Protection Information In Last Bytes (PIILB): If this bit is set to ‘1’, then the<br>namespace supports protection information transferred as the last bytes of<br>4<br>metadata. If this bit is cleared to ‘0’, then the namespace does not support<br>protection information transferred as the last bytes of metadata.<br>Protection Information In First Bytes (PIIFB): If this bit is set to ‘1’, then the<br>namespace supports protection information transferred as the first bytes of<br>metadata. If this bit is cleared to ‘0’, then the namespace does not support<br>3<br>protection information transferred as the first bytes of metadata. For<br>implementations compliant with revision 1.0 or later of the NVM Express NVM<br>Command Set Specification, this bit shall be cleared to ‘0’.<br>Protection Information Type 3 Supported (PIT3S): If this bit is set to ‘1’,<br>then the namespace supports Protection Information Type 3. If this bit is<br>2<br>cleared to ‘0’, then the namespace does not support Protection Information<br>Type 3.<br>Protection Information Type 2 Supported (PIT2S): If this bit is set to ‘1’,<br>then the namespace supports Protection Information Type 2. If cleared to ‘0’<br>1<br>indicates that the namespace does not support Protection Information Type<br>2.<br>Protection Information Type 1 Supported (PIT1S): If this bit is set to ‘1’,<br>then the namespace supports Protection Information Type 1. If this bit is<br>0<br>cleared to ‘0’, then the namespace does not support Protection Information<br>Type 1.||||||Yes||
|||||||||Bits|||Description|||
||||||||7:5|||Reserved||||
||||||||4|||Protection Information In Last Bytes (PIILB): If this bit is set to ‘1’, then the<br>namespace supports protection information transferred as the last bytes of<br>metadata. If this bit is cleared to ‘0’, then the namespace does not support<br>protection information transferred as the last bytes of metadata.||||
||||||||3|||Protection Information In First Bytes (PIIFB): If this bit is set to ‘1’, then the<br>namespace supports protection information transferred as the first bytes of<br>metadata. If this bit is cleared to ‘0’, then the namespace does not support<br>protection information transferred as the first bytes of metadata. For<br>implementations compliant with revision 1.0 or later of the NVM Express NVM<br>Command Set Specification, this bit shall be cleared to ‘0’.||||
||||||||2|||Protection Information Type 3 Supported (PIT3S): If this bit is set to ‘1’,<br>then the namespace supports Protection Information Type 3. If this bit is<br>cleared to ‘0’, then the namespace does not support Protection Information<br>Type 3.||||
||||||||1|||Protection Information Type 2 Supported (PIT2S): If this bit is set to ‘1’,<br>then the namespace supports Protection Information Type 2. If cleared to ‘0’<br>indicates that the namespace does not support Protection Information Type<br>2.||||
||||||||0|||Protection Information Type 1 Supported (PIT1S): If this bit is set to ‘1’,<br>then the namespace supports Protection Information Type 1. If this bit is<br>cleared to ‘0’, then the namespace does not support Protection Information<br>Type 1.||||
|29|||M|||End-to-end Data Protection Type Settings (DPS): This field indicates the protection<br>information Type settings for the end-to-end data protection feature. Refer to section<br>5.3.<br>Bits Description<br>7:4 Reserved<br>Protection Information Position (PIP): If this bit is set to ‘1’, then the<br>protection information, if enabled, is transferred as the first bytes of<br>metadata. If this bit is cleared to ‘0’, then the protection information, if<br>3<br>enabled, is transferred as the last bytes of metadata. For implementations<br>compliant with version 1.0 or later of the NVM Express NVM Command<br>Set Specification, this bit shall be cleared to ‘0’.<br>Protection Information Type (PIT): This field indicates whether<br>protection information is enabled and the type of protection information<br>enabled. The values for this field have the following meanings:<br>Value Definition<br>2:0 000b Protection information is not enabled<br>001b Type 1 protection information is enabled<br>010b Type 2 protection information is enabled<br>011b Type 3 protection information is enabled<br>100b to 111b Reserved||||||No||
|30|||O|||Namespace Multi-path I/O and Namespace Sharing Capabilities (NMIC): This field<br>is as defined in the I/O Command Set Independent Identify Namespace data structure<br>(refer to the I/O Command Set Independent Identify Namespace data structure section<br>in the NVM Express Base Specification).||||||Yes||


||Bits|||Description|
|---|---|---|---|---|
|7:4|||||
|3|||||
|2:0|||||


||Value|||Definition||
|---|---|---|---|---|---|
|000b|||Protection information is not enabled|||
|001b|||Type 1 protection information is enabled|||
|010b|||Type 2 protection information is enabled|||
|011b|||Type 3 protection information is enabled|||
|100b to 111b|||Reserved|||

85

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

O

**Reservation Capabilities (RESCAP): This field is as defined in the I/O Command Set**
Independent Identify Namespace data structure (refer to the I/O Command Set
Independent Identify Namespace data structure section in the NVM Express Base
Specification).
No

O

**Format Progress Indicator (FPI): This field is as defined in the I/O Command Set**
Independent Identify Namespace data structure (refer to the I/O Command Set
Independent Identify Namespace data structure section in the NVM Express Base
Specification).
No

O

**Deallocate Logical Block Features (DLFEAT): This field indicates information about**
features that affect deallocating logical blocks for this namespace.

**Bits**

**Description**
7:5
Reserved

**Guard Deallocation Status (GDS): If this bit is set to ‘1’, then the Guard field**
for deallocated logical blocks that contain protection information is set to the
CRC for the value read from the deallocated logical block and its metadata
(excluding protection information). If this bit is cleared to ‘0’, then each byte in
the Guard field for the deallocated logical blocks that contain protection
information is set to FFh.

**Write Zeroes Deallocation Support (WZDS): If this bit is set to ‘1’, then the**
controller supports the Deallocate bit in the Write Zeroes command for this
namespace. If this bit is cleared to ‘0’, then the controller does not support the
Deallocate bit in the Write Zeroes command for this namespace. This bit shall
be set to the same value for all namespaces in the NVM subsystem.

2:0

**Deallocation Read Behavior (DRB): This field indicates the deallocated logical**
block read behavior. For a logical block that is deallocated, this field indicates
the values read from that deallocated logical block and its metadata (excluding
protection information). The values for this field have the following meanings:

**Value**

**Definition**
000b
The read behavior is not reported
001b
A deallocated logical block returns all bytes cleared to 0h
010b
A deallocated logical block returns all bytes set to FFh
011b to 111b
Reserved
No

35:34
O

**Namespace Atomic Write Unit Normal (NAWUN): This field indicates the namespace**
specific size of the write operation guaranteed to be written atomically to the NVM
during normal operation. If the NSABP bit is cleared to ‘0’, then this field is reserved.
A value of 0h indicates that the size for this namespace is the same size as that reported
in the AWUN field of the Identify Controller data structure. All other values specify a size
in terms of logical blocks using the same encoding as the AWUN field (i.e., with the
exception of the value 0, this field is a 0’s based value). Refer to section 2.1.4.
No

37:36
O

**Namespace Atomic Write Unit Power Fail (NAWUPF): This field indicates the**
namespace specific size of the write operation guaranteed to be written atomically to
the NVM during a power fail or error condition. If the NSABP bit is cleared to ‘0’, then
this field is reserved.
A value of 0h indicates that the size for this namespace is the same size as that reported
in the AWUPF field of the Identify Controller data structure. All other values specify a
size in terms of logical blocks using the same encoding as the AWUPF field (i.e., with
the exception of the value 0, this field is a 0’s based value). Refer to section 2.1.4.
No


||Bytes|||1<br>O/M|||Description|||||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|31|||O|||Reservation Capabilities (RESCAP): This field is as defined in the I/O Command Set<br>Independent Identify Namespace data structure (refer to the I/O Command Set<br>Independent Identify Namespace data structure section in the NVM Express Base<br>Specification).||||||No||
|32|||O|||Format Progress Indicator (FPI): This field is as defined in the I/O Command Set<br>Independent Identify Namespace data structure (refer to the I/O Command Set<br>Independent Identify Namespace data structure section in the NVM Express Base<br>Specification).||||||No||
|33|||O|||Deallocate Logical Block Features (DLFEAT): This field indicates information about<br>features that affect deallocating logical blocks for this namespace.<br>Bits Description<br>7:5 Reserved<br>Guard Deallocation Status (GDS): If this bit is set to ‘1’, then the Guard field<br>for deallocated logical blocks that contain protection information is set to the<br>CRC for the value read from the deallocated logical block and its metadata<br>4<br>(excluding protection information). If this bit is cleared to ‘0’, then each byte in<br>the Guard field for the deallocated logical blocks that contain protection<br>information is set to FFh.<br>Write Zeroes Deallocation Support (WZDS): If this bit is set to ‘1’, then the<br>controller supports the Deallocate bit in the Write Zeroes command for this<br>3 namespace. If this bit is cleared to ‘0’, then the controller does not support the<br>Deallocate bit in the Write Zeroes command for this namespace. This bit shall<br>be set to the same value for all namespaces in the NVM subsystem.<br>Deallocation Read Behavior (DRB): This field indicates the deallocated logical<br>block read behavior. For a logical block that is deallocated, this field indicates<br>the values read from that deallocated logical block and its metadata (excluding<br>protection information). The values for this field have the following meanings:<br>2:0 Value Definition<br>000b The read behavior is not reported<br>001b A deallocated logical block returns all bytes cleared to 0h<br>010b A deallocated logical block returns all bytes set to FFh<br>011b to 111b Reserved||||||No||
|||||||||Bits|||Description|||
||||||||7:5|||Reserved||||
||||||||4|||Guard Deallocation Status (GDS): If this bit is set to ‘1’, then the Guard field<br>for deallocated logical blocks that contain protection information is set to the<br>CRC for the value read from the deallocated logical block and its metadata<br>(excluding protection information). If this bit is cleared to ‘0’, then each byte in<br>the Guard field for the deallocated logical blocks that contain protection<br>information is set to FFh.||||
||||||||3|||Write Zeroes Deallocation Support (WZDS): If this bit is set to ‘1’, then the<br>controller supports the Deallocate bit in the Write Zeroes command for this<br>namespace. If this bit is cleared to ‘0’, then the controller does not support the<br>Deallocate bit in the Write Zeroes command for this namespace. This bit shall<br>be set to the same value for all namespaces in the NVM subsystem.||||
||||||||2:0|||Deallocation Read Behavior (DRB): This field indicates the deallocated logical<br>block read behavior. For a logical block that is deallocated, this field indicates<br>the values read from that deallocated logical block and its metadata (excluding<br>protection information). The values for this field have the following meanings:<br>Value Definition<br>000b The read behavior is not reported<br>001b A deallocated logical block returns all bytes cleared to 0h<br>010b A deallocated logical block returns all bytes set to FFh<br>011b to 111b Reserved||||
|35:34|||O|||Namespace Atomic Write Unit Normal (NAWUN): This field indicates the namespace<br>specific size of the write operation guaranteed to be written atomically to the NVM<br>during normal operation. If the NSABP bit is cleared to ‘0’, then this field is reserved.<br>A value of 0h indicates that the size for this namespace is the same size as that reported<br>in the AWUN field of the Identify Controller data structure. All other values specify a size<br>in terms of logical blocks using the same encoding as the AWUN field (i.e., with the<br>exception of the value 0, this field is a 0’s based value). Refer to section 2.1.4.||||||No||
|37:36|||O|||Namespace Atomic Write Unit Power Fail (NAWUPF): This field indicates the<br>namespace specific size of the write operation guaranteed to be written atomically to<br>the NVM during a power fail or error condition. If the NSABP bit is cleared to ‘0’, then<br>this field is reserved.<br>A value of 0h indicates that the size for this namespace is the same size as that reported<br>in the AWUPF field of the Identify Controller data structure. All other values specify a<br>size in terms of logical blocks using the same encoding as the AWUPF field (i.e., with<br>the exception of the value 0, this field is a 0’s based value). Refer to section 2.1.4.||||||No||


||Value|||Definition||
|---|---|---|---|---|---|
|000b|||The read behavior is not reported|||
|001b|||A deallocated logical block returns all bytes cleared to 0h|||
|010b|||A deallocated logical block returns all bytes set to FFh|||
|011b to 111b|||Reserved|||

86

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

39:38
O

**Namespace Atomic Compare & Write Unit (NACWU): This field indicates the**
namespace specific size of the write operation guaranteed to be written atomically to
the NVM for a Compare and Write fused command. If the NSABP bit is cleared to ‘0’,
then this field is reserved.
A value of 0h indicates that the size for this namespace is the same size as that reported
in the ACWU field of the Identify Controller data structure. All other values specify a size
in terms of logical blocks using the same encoding as the ACWU field (i.e., with the
exception of the value 0, this field is a 0’s based value). Refer to section 2.1.4.
No

41:40
O

**Namespace Atomic Boundary Size Normal (NABSN): This field indicates the atomic**
boundary size for this namespace for the NAWUN value. This field is specified in logical
blocks. Writes to this namespace that cross atomic boundaries are not guaranteed to
be atomic to the NVM with respect to other read or write commands.
A value of 0h indicates that there are no atomic boundaries for normal write operations.
All other values specify a size in terms of logical blocks using the same encoding as the
AWUN field (i.e., with the exception of the value 0, this field is a 0’s based value). Refer
to section 2.1.4.
Refer to section 5.2.2 for how this field is utilized.
No

43:42
O

**Namespace Atomic Boundary Offset (NABO): This field indicates the LBA on this**
namespace where the first atomic boundary starts.
If the NABSN and NABSPF fields are cleared to 0h, then the NABO field shall be cleared
to 0h. NABO shall be less than or equal to NABSN and NABSPF. Refer to section 2.1.4.
Refer to section 5.2.2 for how this field is utilized.
No

45:44
O

**Namespace Atomic Boundary Size Power Fail (NABSPF): This field indicates the**
atomic boundary size for this namespace specific to the Namespace Atomic Write Unit
Power Fail value. This field is specified in logical blocks. Writes to this namespace that
cross atomic boundaries are not guaranteed to be atomic with respect to other read or
write commands and there is no guarantee of data returned on subsequent reads of the
associated logical blocks.
A value of 0h indicates that there are no atomic boundaries for power fail or error
conditions. All other values specify a size in terms of logical blocks using the same
encoding as the AWUPF field (i.e., with the exception of the value 0, this field is a 0’s

**based value). Refer to section 2.1.4.**
No

47:46
O

**Namespace Optimal I/O Boundary (NOIOB): This field indicates the optimal I/O**
boundary for this namespace. This field is specified in logical blocks. The host should
construct read and write commands that do not cross the I/O boundary to achieve
optimal performance. A value of 0h indicates that no optimal I/O boundary is reported.
Refer to section 5.2.2 for how this field is utilized to improve performance and
endurance.
No


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|39:38|||O|||Namespace Atomic Compare & Write Unit (NACWU): This field indicates the<br>namespace specific size of the write operation guaranteed to be written atomically to<br>the NVM for a Compare and Write fused command. If the NSABP bit is cleared to ‘0’,<br>then this field is reserved.<br>A value of 0h indicates that the size for this namespace is the same size as that reported<br>in the ACWU field of the Identify Controller data structure. All other values specify a size<br>in terms of logical blocks using the same encoding as the ACWU field (i.e., with the<br>exception of the value 0, this field is a 0’s based value). Refer to section 2.1.4.|||No|||
|41:40|||O|||Namespace Atomic Boundary Size Normal (NABSN): This field indicates the atomic<br>boundary size for this namespace for the NAWUN value. This field is specified in logical<br>blocks. Writes to this namespace that cross atomic boundaries are not guaranteed to<br>be atomic to the NVM with respect to other read or write commands.<br>A value of 0h indicates that there are no atomic boundaries for normal write operations.<br>All other values specify a size in terms of logical blocks using the same encoding as the<br>AWUN field (i.e., with the exception of the value 0, this field is a 0’s based value). Refer<br>to section 2.1.4.<br>Refer to section 5.2.2 for how this field is utilized.|||No|||
|43:42|||O|||Namespace Atomic Boundary Offset (NABO): This field indicates the LBA on this<br>namespace where the first atomic boundary starts.<br>If the NABSN and NABSPF fields are cleared to 0h, then the NABO field shall be cleared<br>to 0h. NABO shall be less than or equal to NABSN and NABSPF. Refer to section 2.1.4.<br>Refer to section 5.2.2 for how this field is utilized.|||No|||
|45:44|||O|||Namespace Atomic Boundary Size Power Fail (NABSPF): This field indicates the<br>atomic boundary size for this namespace specific to the Namespace Atomic Write Unit<br>Power Fail value. This field is specified in logical blocks. Writes to this namespace that<br>cross atomic boundaries are not guaranteed to be atomic with respect to other read or<br>write commands and there is no guarantee of data returned on subsequent reads of the<br>associated logical blocks.<br>A value of 0h indicates that there are no atomic boundaries for power fail or error<br>conditions. All other values specify a size in terms of logical blocks using the same<br>encoding as the AWUPF field (i.e., with the exception of the value 0, this field is a 0’s<br>based value). Refer to section 2.1.4.|||No|||
|47:46|||O|||Namespace Optimal I/O Boundary (NOIOB): This field indicates the optimal I/O<br>boundary for this namespace. This field is specified in logical blocks. The host should<br>construct read and write commands that do not cross the I/O boundary to achieve<br>optimal performance. A value of 0h indicates that no optimal I/O boundary is reported.<br>Refer to section 5.2.2 for how this field is utilized to improve performance and<br>endurance.|||No|||

87

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

63:48
O

**NVM Capacity (NVMCAP): This field indicates the total size of the NVM allocated to**
this namespace. The value is in bytes. This field shall be supported if the Namespace
Management capability (refer to section 5.6) is supported.
Note: This field may not correspond to the logical block size multiplied by the
Namespace Size field. Due to thin provisioning or other settings (e.g., endurance), this
field may be larger or smaller than the product of the logical block size and the
Namespace Size reported.
If the controller supports Asymmetric Namespace Access Reporting (refer to the CMIC
field), and the relationship between the controller and the namespace is in the ANA
Inaccessible state (refer to the ANA Inaccessible state section in the NVM Express
Base Specification) or the ANA Persistent Loss state (refer to the ANA Persistent Loss
state section in the NVM Express Base Specification), then this field shall be cleared to
0h.
No

65:64
O

**Namespace Preferred Write Granularity (NPWG): This field indicates the smallest**
recommended write granularity in logical blocks for this namespace. This is a 0’s based
value. If this field is not supported as indicated by the OPTPERF field, then this field is
reserved.
The size indicated by this field should be less than or equal to the maximum number of
logical blocks that are able to be transferred based on the value of the Maximum Data
Transfer Size (MDTS) field defined in the Identify Controller data structure (refer to the

memory page size. The value of this field may change if the namespace is reformatted.
The size should be a multiple of the Namespace Preferred Write Alignment (NPWA)
field.
Refer to section 5.2.2 for how this field is utilized to improve performance and

**endurance.**
No

67:66
O

**Namespace Preferred Write Alignment (NPWA): This field indicates the**
recommended write alignment in logical blocks for this namespace. This is a 0’s based
value. If this field is not supported as indicated by the OPTPERF field, then this field is
reserved.
The value of this field may change if the namespace is reformatted.
Refer to section 5.2.2 for how this field is utilized to improve performance and

**endurance.**
No

69:68
O

**Namespace Preferred Deallocate Granularity (NPDG): This field indicates the**
recommended granularity in logical blocks for the Dataset Management command with
the Attribute – Deallocate bit set to ‘1’ in Dword 11. This is a 0’s based value. If this field
is not supported as indicated by the OPTPERF field, then this field is reserved.
The value of this field may change if the namespace is reformatted. The size should be
a multiple of the Namespace Preferred Deallocate Alignment (NPDA) field.
Refer to section 5.2.2 for how this field is utilized to improve performance and

**endurance.**
No

71:70
O

**Namespace Preferred Deallocate Alignment (NPDA): This field indicates the**
recommended alignment in logical blocks for the Dataset Management command with
the Attribute – Deallocate bit set to ‘1’ in Dword 11. This is a 0’s based value. If this field
is not supported as indicated by the OPTPERF field, then this field is reserved.
The value of this field may change if the namespace is reformatted.
Refer to section 5.2.2 for how this field is utilized to improve performance and

**endurance.**
No


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|63:48|||O|||NVM Capacity (NVMCAP): This field indicates the total size of the NVM allocated to<br>this namespace. The value is in bytes. This field shall be supported if the Namespace<br>Management capability (refer to section 5.6) is supported.<br>Note: This field may not correspond to the logical block size multiplied by the<br>Namespace Size field. Due to thin provisioning or other settings (e.g., endurance), this<br>field may be larger or smaller than the product of the logical block size and the<br>Namespace Size reported.<br>If the controller supports Asymmetric Namespace Access Reporting (refer to the CMIC<br>field), and the relationship between the controller and the namespace is in the ANA<br>Inaccessible state (refer to the ANA Inaccessible state section in the NVM Express<br>Base Specification) or the ANA Persistent Loss state (refer to the ANA Persistent Loss<br>state section in the NVM Express Base Specification), then this field shall be cleared to<br>0h.|||No|||
|65:64|||O|||Namespace Preferred Write Granularity (NPWG): This field indicates the smallest<br>recommended write granularity in logical blocks for this namespace. This is a 0’s based<br>value. If this field is not supported as indicated by the OPTPERF field, then this field is<br>reserved.<br>The size indicated by this field should be less than or equal to the maximum number of<br>logical blocks that are able to be transferred based on the value of the Maximum Data<br>Transfer Size (MDTS) field defined in the Identify Controller data structure (refer to the<br>NVM Express Base Specification). The MDTS field specified in units of minimum<br>memory page size. The value of this field may change if the namespace is reformatted.<br>The size should be a multiple of the Namespace Preferred Write Alignment (NPWA)<br>field.<br>Refer to section 5.2.2 for how this field is utilized to improve performance and<br>endurance.|||No|||
|67:66|||O|||Namespace Preferred Write Alignment (NPWA): This field indicates the<br>recommended write alignment in logical blocks for this namespace. This is a 0’s based<br>value. If this field is not supported as indicated by the OPTPERF field, then this field is<br>reserved.<br>The value of this field may change if the namespace is reformatted.<br>Refer to section 5.2.2 for how this field is utilized to improve performance and<br>endurance.|||No|||
|69:68|||O|||Namespace Preferred Deallocate Granularity (NPDG): This field indicates the<br>recommended granularity in logical blocks for the Dataset Management command with<br>the Attribute – Deallocate bit set to ‘1’ in Dword 11. This is a 0’s based value. If this field<br>is not supported as indicated by the OPTPERF field, then this field is reserved.<br>The value of this field may change if the namespace is reformatted. The size should be<br>a multiple of the Namespace Preferred Deallocate Alignment (NPDA) field.<br>Refer to section 5.2.2 for how this field is utilized to improve performance and<br>endurance.|||No|||
|71:70|||O|||Namespace Preferred Deallocate Alignment (NPDA): This field indicates the<br>recommended alignment in logical blocks for the Dataset Management command with<br>the Attribute – Deallocate bit set to ‘1’ in Dword 11. This is a 0’s based value. If this field<br>is not supported as indicated by the OPTPERF field, then this field is reserved.<br>The value of this field may change if the namespace is reformatted.<br>Refer to section 5.2.2 for how this field is utilized to improve performance and<br>endurance.|||No|||

88

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

73:72
O

**Namespace Optimal Write Size (NOWS): This field indicates the size in logical blocks**
for optimal write performance for this namespace. This is a 0’s based value. If this field
is not supported as indicated by the OPTPERF field, then this field is reserved.
If this namespace is associated with an NVM Set and:
a)
this field is supported as defined by the OPTPERF field, then this field shall be
set to the number of logical blocks corresponding to the Optimal Write Size
field in the NVM Set Attributes Entry (refer to the Namespace Identification
Descriptor in the NVM Express Base Specification) for that NVM Set; or
b)
this field is not supported as defined by the OPTPERF field, then the host
should use the Optimal Write Size field in the NVM Set Attributes Entry for that
NVM Set for I/O optimization (refer to section 5.2.2).
The size indicated should be less than or equal to the maximum number of logical
blocks that are able to be transferred based on the value of the Maximum Data Transfer
Size (MDTS) field defined in the Identify Controller data structure (refer to the NVM
Express Base Specification). The MDTS field is specified in units of minimum memory
page size.The value of this field may change if the namespace is reformatted. The value
of this field should be a multiple of the Namespace Preferred Write Granularity (NPWG)
field.
Refer to section 5.2.2 for how this field is utilized to improve performance and

**endurance.**
No

75:74
O

**Maximum Single Source Range Length (MSSRL): This field indicates the maximum**
number of logical blocks that may be specified in the Number of Logical Blocks field in
each valid Source Range Entries Descriptor of a Copy command (refer to section 3.3.2).
If the controller supports the Copy command, then this field shall be set to a non-zero
value.
No

79:76
O

**Maximum Copy Length (MCL): This field indicates the maximum number of logical**
blocks that may be specified in a Copy command (i.e., the sum of the number of logical
blocks specified in all Source Range entries).
If the controller supports the Copy command, then this field shall be set to a non-zero
value.
No

O

**Maximum Source Range Count (MSRC): This field indicates the maximum number**
of Source Range entries that may be used to specify source data in a Copy command.
This is a 0’s based value.
No

O

**Key Per I/O Status (KPIOS): This field indicates namespace Key Per I/O capability**
status.

**Bits**

**Description**
7:2
Reserved

**Key Per I/O Supported in Namespace (KPIOSNS): If this bit is set to ‘1’, then**
the Key Per I/O capability is supported by the namespace. If this bit is cleared
to ‘0’, then the Key Per I/O capability is not supported by the namespace.

**Key Per I/O Enabled in Namespace (KPIOENS): If this bit is set to ‘1’, then**
the Key Per I/O capability is enabled on the namespace. The mechanism to
enable the Key Per I/O capability on the namespace is outside the scope of
this specification (refer to section 5.4). If this bit is cleared to ‘0’, then the Key
Per I/O capability is disabled on the namespace.

**If the KPIOSNS bit is cleared to ‘0’, then this bit shall be cleared to ‘0’.**
No


||Bytes|||1<br>O/M|||Description|||||||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|73:72|||O|||Namespace Optimal Write Size (NOWS): This field indicates the size in logical blocks<br>for optimal write performance for this namespace. This is a 0’s based value. If this field<br>is not supported as indicated by the OPTPERF field, then this field is reserved.<br>If this namespace is associated with an NVM Set and:<br>a) this field is supported as defined by the OPTPERF field, then this field shall be<br>set to the number of logical blocks corresponding to the Optimal Write Size<br>field in the NVM Set Attributes Entry (refer to the Namespace Identification<br>Descriptor in the NVM Express Base Specification) for that NVM Set; or<br>b) this field is not supported as defined by the OPTPERF field, then the host<br>should use the Optimal Write Size field in the NVM Set Attributes Entry for that<br>NVM Set for I/O optimization (refer to section 5.2.2).<br>The size indicated should be less than or equal to the maximum number of logical<br>blocks that are able to be transferred based on the value of the Maximum Data Transfer<br>Size (MDTS) field defined in the Identify Controller data structure (refer to the NVM<br>Express Base Specification). The MDTS field is specified in units of minimum memory<br>page size.The value of this field may change if the namespace is reformatted. The value<br>of this field should be a multiple of the Namespace Preferred Write Granularity (NPWG)<br>field.<br>Refer to section 5.2.2 for how this field is utilized to improve performance and<br>endurance.|||||||No|||
|75:74|||O|||Maximum Single Source Range Length (MSSRL): This field indicates the maximum<br>number of logical blocks that may be specified in the Number of Logical Blocks field in<br>each valid Source Range Entries Descriptor of a Copy command (refer to section 3.3.2).<br>If the controller supports the Copy command, then this field shall be set to a non-zero<br>value.|||||||No|||
|79:76|||O|||Maximum Copy Length (MCL): This field indicates the maximum number of logical<br>blocks that may be specified in a Copy command (i.e., the sum of the number of logical<br>blocks specified in all Source Range entries).<br>If the controller supports the Copy command, then this field shall be set to a non-zero<br>value.|||||||No|||
|80|||O|||Maximum Source Range Count (MSRC): This field indicates the maximum number<br>of Source Range entries that may be used to specify source data in a Copy command.<br>This is a 0’s based value.|||||||No|||
|81|||O|||Key Per I/O Status (KPIOS): This field indicates namespace Key Per I/O capability<br>status.<br>Bits Description<br>7:2 Reserved<br>Key Per I/O Supported in Namespace (KPIOSNS): If this bit is set to ‘1’, then<br>1 the Key Per I/O capability is supported by the namespace. If this bit is cleared<br>to ‘0’, then the Key Per I/O capability is not supported by the namespace.<br>Key Per I/O Enabled in Namespace (KPIOENS): If this bit is set to ‘1’, then<br>the Key Per I/O capability is enabled on the namespace. The mechanism to<br>enable the Key Per I/O capability on the namespace is outside the scope of<br>0 this specification (refer to section 5.4). If this bit is cleared to ‘0’, then the Key<br>Per I/O capability is disabled on the namespace.<br>If the KPIOSNS bit is cleared to ‘0’, then this bit shall be cleared to ‘0’.|||||||No|||
|||||||||Bits|||Description|||||
||||||||7:2|||Reserved||||||
||||||||1|||Key Per I/O Supported in Namespace (KPIOSNS): If this bit is set to ‘1’, then<br>the Key Per I/O capability is supported by the namespace. If this bit is cleared<br>to ‘0’, then the Key Per I/O capability is not supported by the namespace.||||||
||||||||0|||Key Per I/O Enabled in Namespace (KPIOENS): If this bit is set to ‘1’, then<br>the Key Per I/O capability is enabled on the namespace. The mechanism to<br>enable the Key Per I/O capability on the namespace is outside the scope of<br>this specification (refer to section 5.4). If this bit is cleared to ‘0’, then the Key<br>Per I/O capability is disabled on the namespace.<br>If the KPIOSNS bit is cleared to ‘0’, then this bit shall be cleared to ‘0’.||||||

89

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

M

**Number of Unique Attribute LBA Formats (NULBAF): This field defines the number**
of supported user data size and metadata size combinations supported by the
namespace that may not share the same host-selectable attributes. These LBA formats
shall be allocated in order (starting at the first index after the LBA formats defined by
the NLBAF field) and packed sequentially (refer to section 5.5).
Refer to section 5.5 for the structure of the LBA formats, the association to the NLBAF
field, and the maximum value of this field.
Yes

Reserved

87:84
O

**Key Per I/O Data Access Alignment and Granularity (KPIODAAG): This field**
indicates the alignment and granularity in logical blocks that is required for commands
that support a KPIOTAG value in the CETYPE field (refer to the Key Per I/O section in
the NVM Express Base Specification).
This is a 0’s based value.
Refer to section 5.4 on the behavior of commands not meeting the alignment or
granularity defined by this field.
The value of this field may change if the namespace is reformatted.
If the KPIOSNS bit is cleared to ‘0’ in the I/O Command Set Independent Identify
Namespace data structure (refer to the NVM Express Base Specification), then this field

**is reserved.**
No

91:88
Reserved

95:92
O

**ANA Group Identifier (ANAGRPID): This field is as defined in the I/O Command Set**
Independent Identify Namespace data structure (refer to the I/O Command Set
Independent Identify Namespace data structure section in the NVM Express Base
Specification).
No

98:96
Reserved

O

**Namespace Attributes (NSATTR): This field is as defined in the I/O Command Set**
Independent Identify Namespace data structure (refer to the I/O Command Set
Independent Identify Namespace data structure section in the NVM Express Base
Specification).
No

101:100
O

**NVM Set Identifier (NVMSETID): This field is as defined in the I/O Command Set**
Independent Identify Namespace data structure (refer to the I/O Command Set
Independent Identify Namespace data structure section in the NVM Express Base
Specification).
No

103:102
O

**Endurance Group Identifier (ENDGID): This field is as defined in the I/O Command**
Set Independent Identify Namespace data structure (refer to the I/O Command Set
Independent Identify Namespace data structure section in the NVM Express Base

**Specification).**
No


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|82|||M|||Number of Unique Attribute LBA Formats (NULBAF): This field defines the number<br>of supported user data size and metadata size combinations supported by the<br>namespace that may not share the same host-selectable attributes. These LBA formats<br>shall be allocated in order (starting at the first index after the LBA formats defined by<br>the NLBAF field) and packed sequentially (refer to section 5.5).<br>Refer to section 5.5 for the structure of the LBA formats, the association to the NLBAF<br>field, and the maximum value of this field.|||Yes|||
|83||||||Reserved||||||
|87:84|||O|||Key Per I/O Data Access Alignment and Granularity (KPIODAAG): This field<br>indicates the alignment and granularity in logical blocks that is required for commands<br>that support a KPIOTAG value in the CETYPE field (refer to the Key Per I/O section in<br>the NVM Express Base Specification).<br>This is a 0’s based value.<br>Refer to section 5.4 on the behavior of commands not meeting the alignment or<br>granularity defined by this field.<br>The value of this field may change if the namespace is reformatted.<br>If the KPIOSNS bit is cleared to ‘0’ in the I/O Command Set Independent Identify<br>Namespace data structure (refer to the NVM Express Base Specification), then this field<br>is reserved.|||No|||
|91:88||||||Reserved||||||
|95:92|||O|||ANA Group Identifier (ANAGRPID): This field is as defined in the I/O Command Set<br>Independent Identify Namespace data structure (refer to the I/O Command Set<br>Independent Identify Namespace data structure section in the NVM Express Base<br>Specification).|||No|||
|98:96||||||Reserved||||||
|99|||O|||Namespace Attributes (NSATTR): This field is as defined in the I/O Command Set<br>Independent Identify Namespace data structure (refer to the I/O Command Set<br>Independent Identify Namespace data structure section in the NVM Express Base<br>Specification).|||No|||
|101:100|||O|||NVM Set Identifier (NVMSETID): This field is as defined in the I/O Command Set<br>Independent Identify Namespace data structure (refer to the I/O Command Set<br>Independent Identify Namespace data structure section in the NVM Express Base<br>Specification).|||No|||
|103:102|||O|||Endurance Group Identifier (ENDGID): This field is as defined in the I/O Command<br>Set Independent Identify Namespace data structure (refer to the I/O Command Set<br>Independent Identify Namespace data structure section in the NVM Express Base<br>Specification).|||No|||

90

**Figure 114: Identify – Identify Namespace Data Structure, NVM Command Set**

**Bytes**

**O/M1**

**Description**

**Reported2**

119:104
O

**Namespace Globally Unique Identifier (NGUID): This field contains a 128-bit value**
that is globally unique and assigned to the namespace when the namespace is created.
This field remains fixed throughout the life of the namespace and is preserved across
namespace and controller operations (e.g., Controller Level Reset, namespace format,
etc.).
This field uses the EUI-64 based 16-byte designator format. Bytes 114:112 contain the
24-bit Organizationally Unique Identifier (OUI) value assigned by the IEEE Registration
Authority. Bytes 119:115 contain an extension identifier assigned by the corresponding
organization. Bytes 111:104 contain the vendor specific extension identifier assigned
by the corresponding organization. Refer to the IEEE EUI-64 guidelines for more
information. This field is big endian (refer to the Namespace Globally Unique Identifier
section in the NVM Express Base Specification).
The controller shall specify a globally unique namespace identifier in this field, the
EUI64 field, or a Namespace UUID in the Namespace Identification Descriptor (refer to
the Namespace Identification Descriptor figure in the NVM Express Base Specification)
when the namespace is created. If the controller is not able to provide a globally unique
identifier in this field, then this field shall be cleared to 0h. Refer to the Unique Identifier

**section in the NVM Express Base Specification.**
No

127:120
O

**IEEE Extended Unique Identifier (EUI64): This field contains a 64-bit IEEE Extended**
Unique Identifier (EUI-64) that is globally unique and assigned to the namespace when
the namespace is created. This field remains fixed throughout the life of the namespace
and is preserved across namespace and controller operations (e.g., Controller Level
Reset, namespace format, etc.).
The EUI-64 is a concatenation of a 24-bit or 36-bit Organizationally Unique Identifier
(OUI or OUI-36) value assigned by the IEEE Registration Authority and an extension
identifier assigned by the corresponding organization. Refer to the IEEE EUI-64
guidelines for more information. This field is big endian (refer to the IEEE Extended
Unique Identifier section in the NVM Express Base Specification).
The controller shall specify a globally unique namespace identifier in this field, the
NGUID field, or a Namespace UUID in the Namespace Identification Descriptor (refer
to the Namespace Identification Descriptor figure in the NVM Express Base
Specification) when the namespace is created. If the controller is not able to provide a
globally unique 64-bit identifier in this field, then this field shall be cleared to 0h. Refer
to the Unique Identifier section in the NVM Express Base Specification.
No

**LBA Formats (refer to section 5.5)**

131:128
M

**LBA Format 0 Support (LBAF0): This field indicates the LBA format 0 that is supported**
by the controller. The LBA format field is defined in Figure 116.
Additional information may be provided in the ELBAF0 field (refer to Figure 118).
Yes

135:132
O

**LBA Format 1 Support (LBAF1): This field indicates the LBA format 1 that is supported**
by the controller. The LBA format field is defined in Figure 116.

**Additional information may be provided in the ELBAF1 field (refer to Figure 118).**
Yes

**…**

383:380
O

**LBA Format 63 Support (LBAF63): This field indicates the LBA format 63 that is**
supported by the controller. The LBA format field is defined in Figure 116.
Additional information may be provided in the ELBAF63 field (refer to Figure 118).
Yes

4095:384
O

**Vendor Specific (VS)**
No
Notes:
1.
O/M definition: O = Optional, M = Mandatory.
2.
Identifies fields that report information for the Identify command when querying the capabilities of LBA formats.


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|119:104|||O|||Namespace Globally Unique Identifier (NGUID): This field contains a 128-bit value<br>that is globally unique and assigned to the namespace when the namespace is created.<br>This field remains fixed throughout the life of the namespace and is preserved across<br>namespace and controller operations (e.g., Controller Level Reset, namespace format,<br>etc.).<br>This field uses the EUI-64 based 16-byte designator format. Bytes 114:112 contain the<br>24-bit Organizationally Unique Identifier (OUI) value assigned by the IEEE Registration<br>Authority. Bytes 119:115 contain an extension identifier assigned by the corresponding<br>organization. Bytes 111:104 contain the vendor specific extension identifier assigned<br>by the corresponding organization. Refer to the IEEE EUI-64 guidelines for more<br>information. This field is big endian (refer to the Namespace Globally Unique Identifier<br>section in the NVM Express Base Specification).<br>The controller shall specify a globally unique namespace identifier in this field, the<br>EUI64 field, or a Namespace UUID in the Namespace Identification Descriptor (refer to<br>the Namespace Identification Descriptor figure in the NVM Express Base Specification)<br>when the namespace is created. If the controller is not able to provide a globally unique<br>identifier in this field, then this field shall be cleared to 0h. Refer to the Unique Identifier<br>section in the NVM Express Base Specification.|||No|||
|127:120|||O|||IEEE Extended Unique Identifier (EUI64): This field contains a 64-bit IEEE Extended<br>Unique Identifier (EUI-64) that is globally unique and assigned to the namespace when<br>the namespace is created. This field remains fixed throughout the life of the namespace<br>and is preserved across namespace and controller operations (e.g., Controller Level<br>Reset, namespace format, etc.).<br>The EUI-64 is a concatenation of a 24-bit or 36-bit Organizationally Unique Identifier<br>(OUI or OUI-36) value assigned by the IEEE Registration Authority and an extension<br>identifier assigned by the corresponding organization. Refer to the IEEE EUI-64<br>guidelines for more information. This field is big endian (refer to the IEEE Extended<br>Unique Identifier section in the NVM Express Base Specification).<br>The controller shall specify a globally unique namespace identifier in this field, the<br>NGUID field, or a Namespace UUID in the Namespace Identification Descriptor (refer<br>to the Namespace Identification Descriptor figure in the NVM Express Base<br>Specification) when the namespace is created. If the controller is not able to provide a<br>globally unique 64-bit identifier in this field, then this field shall be cleared to 0h. Refer<br>to the Unique Identifier section in the NVM Express Base Specification.|||No|||
||LBA Formats (refer to section 5.5)|||||||||||
|131:128|||M|||LBA Format 0 Support (LBAF0): This field indicates the LBA format 0 that is supported<br>by the controller. The LBA format field is defined in Figure 116.<br>Additional information may be provided in the ELBAF0 field (refer to Figure 118).|||Yes|||
|135:132|||O|||LBA Format 1 Support (LBAF1): This field indicates the LBA format 1 that is supported<br>by the controller. The LBA format field is defined in Figure 116.<br>Additional information may be provided in the ELBAF1 field (refer to Figure 118).|||Yes|||
|…||||||||||||
|383:380|||O|||LBA Format 63 Support (LBAF63): This field indicates the LBA format 63 that is<br>supported by the controller. The LBA format field is defined in Figure 116.<br>Additional information may be provided in the ELBAF63 field (refer to Figure 118).|||Yes|||
|4095:384|||O|||Vendor Specific (VS)|||No|||
|Notes:<br>1. O/M definition: O = Optional, M = Mandatory.<br>2. Identifies fields that report information for the Identify command when querying the capabilities of LBA formats.||||||||||||

91

**Figure 115: Namespace Alignment and Granularity Attributes**

**Field**

**Supported**

**Optimal Write Performance Value**

**00b**

**01b**

**10b**

**11b**
NPWG
No
Yes
Yes
Yes
NPWA
No
Yes
Yes
Yes
NPDG
No
Yes
No
Yes
NPDA
No
Yes
Yes
Yes
NPDGL
No
No
Yes
Yes
NPDAL
No
No
Yes
Yes
NOWS
No
Yes
Yes
Yes
The use of these fields by the host for I/O optimization is described in section 5.2.2.

The LBA format data structure is described in Figure 116.

**Figure 116: LBA Format Data Structure, NVM Command Set Specific**

**Bits**

**Description**
31:26

**Reserved**

25:24
Relative Performance (RP): This field indicates the relative performance of the LBA format indicated
relative to other LBA formats supported by the controller. Depending on the size of the LBA and
associated metadata, there may be performance implications. The performance analysis is based on
better performance on a queue depth 32 with 4 KiB read workload. The meanings of the values indicated
are included in the following table.

**Value**

**Definition**
00b
Best performance
01b
Better performance
10b
Good performance
11b
Degraded performance

23:16
LBA Data Size (LBADS): This field indicates the LBA data size supported. The value is reported in terms
of a power of two (2^n). A non-zero value less than 9 (i.e., 512 bytes) is not supported. If the value

**reported is 0h, then the LBA format is not currently available (refer to section 5.5).**

15:00

**Metadata Size (MS): This field indicates the number of metadata bytes provided per LBA-based on the**
LBA Data Size indicated. If there is no metadata supported, then this field shall be cleared to 0h.
If metadata is supported, then the namespace may support the metadata being transferred as part of an
extended data LBA or as part of a separate contiguous buffer. If end-to-end data protection is enabled,
then the first eight bytes or last eight bytes of the metadata is the protection information (refer to the DPS

**field in the Identify Namespace data structure).**

**4.1.5.2**

**I/O Command Set specific fields within Identify Controller data structure (CNS 01h)**
The following table describes the NVM Command Set specific fields within the Identify Controller data
structure described in the NVM Express Base Specification.

**Figure 117: Identify – Identify Controller data structure, NVM Command Set Specific Fields**

**Bytes**

**O/M1**

**Description**
…


||Field|||Optimal Write Performance Value|||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Supported|||00b|||01b|||10b|||11b||
|NPWG|||No|||Yes|||Yes|||Yes|||
|NPWA|||No|||Yes|||Yes|||Yes|||
|NPDG|||No|||Yes|||No|||Yes|||
|NPDA|||No|||Yes|||Yes|||Yes|||
|NPDGL|||No|||No|||Yes|||Yes|||
|NPDAL|||No|||No|||Yes|||Yes|||
|NOWS|||No|||Yes|||Yes|||Yes|||
|The use of these fields by the host for I/O optimization is described in section 5.2.2.|||||||||||||||


||Bits|||Description||
|---|---|---|---|---|---|
|31:26|||Reserved|||
|25:24|||Relative Performance (RP): This field indicates the relative performance of the LBA format indicated<br>relative to other LBA formats supported by the controller. Depending on the size of the LBA and<br>associated metadata, there may be performance implications. The performance analysis is based on<br>better performance on a queue depth 32 with 4 KiB read workload. The meanings of the values indicated<br>are included in the following table.<br>Value Definition<br>00b Best performance<br>01b Better performance<br>10b Good performance<br>11b Degraded performance|||
|23:16|||LBA Data Size (LBADS): This field indicates the LBA data size supported. The value is reported in terms<br>of a power of two (2^n). A non-zero value less than 9 (i.e., 512 bytes) is not supported. If the value<br>reported is 0h, then the LBA format is not currently available (refer to section 5.5).|||
|15:00|||Metadata Size (MS): This field indicates the number of metadata bytes provided per LBA-based on the<br>LBA Data Size indicated. If there is no metadata supported, then this field shall be cleared to 0h.<br>If metadata is supported, then the namespace may support the metadata being transferred as part of an<br>extended data LBA or as part of a separate contiguous buffer. If end-to-end data protection is enabled,<br>then the first eight bytes or last eight bytes of the metadata is the protection information (refer to the DPS<br>field in the Identify Namespace data structure).|||


||Value|||Definition||
|---|---|---|---|---|---|
|00b|||Best performance|||
|01b|||Better performance|||
|10b|||Good performance|||
|11b|||Degraded performance|||


||Bytes|||1<br>O/M|||Description||
|---|---|---|---|---|---|---|---|---|
|…|||||||||

92

**Figure 117: Identify – Identify Controller data structure, NVM Command Set Specific Fields**

**Bytes**

**O/M1**

**Description**

527:526
M

**Atomic Write Unit Normal (AWUN): This field indicates the size of the write operation**
guaranteed to be written atomically to the NVM across all namespaces with any supported
namespace format during normal operation. This field is specified in logical blocks and is a 0’s
based value.
If a specific namespace guarantees a larger size than is reported in this field, then this
namespace specific size is reported in the NAWUN field in the Identify Namespace data structure.
Refer to section 2.1.4.
If a write command is submitted that has a size less than or equal to the AWUN value, the host
is guaranteed that the write command is atomic to the NVM with respect to other read or write
commands. If a write command is submitted that has a size greater than the AWUN value, then
there is no guarantee of command atomicity, but atomicity is guaranteed for portions of the
command if the command is processed in Multiple Atomicity Mode (refer to section 2.1.4.5).
AWUN does not have any applicability to write errors caused by power failure (refer to Atomic
Write Unit Power Fail).
For any write command other than the Copy command, a value of FFFFh indicates the command
is always atomic as this is the largest command size. For a Copy command, a value of FFFFh
indicates that the atomicity of the write portion of the Copy command is 10000h logical blocks. It
is recommended that implementations support a minimum of 128 KiB (appropriately scaled
based on logical block size).

529:528
M

**Atomic Write Unit Power Fail (AWUPF): This field indicates the size of the write operation**
guaranteed to be written atomically to the NVM across all namespaces with any supported
namespace format during a power fail or error condition.
If a specific namespace guarantees a larger size than is reported in this field, then this
namespace specific size is reported in the NAWUPF field in the Identify Namespace data
structure. Refer to section 2.1.4.
This field is specified in logical blocks and is a 0’s based value. The AWUPF value shall be less
than or equal to the AWUN value.
If a write command is submitted that has a size less than or equal to the AWUPF value, the host
is guaranteed that the write is atomic to the NVM with respect to other read or write commands.
If a write command is submitted that is greater than this size, there is no guarantee of command
atomicity, but atomicity is guaranteed for portions of the command if the command is processed
in Multiple Atomicity Mode (refer to section 2.1.4.5). If the write size is less than or equal to the
AWUPF value and the write command fails, then subsequent read commands for the associated
logical blocks shall return data from the previous successful write command. If a write command
is submitted that has a size greater than the AWUPF value, then there is no guarantee of data
returned on subsequent reads of the associated logical blocks.
…


||Bytes|||1<br>O/M|||Description||
|---|---|---|---|---|---|---|---|---|
|527:526|||M|||Atomic Write Unit Normal (AWUN): This field indicates the size of the write operation<br>guaranteed to be written atomically to the NVM across all namespaces with any supported<br>namespace format during normal operation. This field is specified in logical blocks and is a 0’s<br>based value.<br>If a specific namespace guarantees a larger size than is reported in this field, then this<br>namespace specific size is reported in the NAWUN field in the Identify Namespace data structure.<br>Refer to section 2.1.4.<br>If a write command is submitted that has a size less than or equal to the AWUN value, the host<br>is guaranteed that the write command is atomic to the NVM with respect to other read or write<br>commands. If a write command is submitted that has a size greater than the AWUN value, then<br>there is no guarantee of command atomicity, but atomicity is guaranteed for portions of the<br>command if the command is processed in Multiple Atomicity Mode (refer to section 2.1.4.5).<br>AWUN does not have any applicability to write errors caused by power failure (refer to Atomic<br>Write Unit Power Fail).<br>For any write command other than the Copy command, a value of FFFFh indicates the command<br>is always atomic as this is the largest command size. For a Copy command, a value of FFFFh<br>indicates that the atomicity of the write portion of the Copy command is 10000h logical blocks. It<br>is recommended that implementations support a minimum of 128 KiB (appropriately scaled<br>based on logical block size).|||
|529:528|||M|||Atomic Write Unit Power Fail (AWUPF): This field indicates the size of the write operation<br>guaranteed to be written atomically to the NVM across all namespaces with any supported<br>namespace format during a power fail or error condition.<br>If a specific namespace guarantees a larger size than is reported in this field, then this<br>namespace specific size is reported in the NAWUPF field in the Identify Namespace data<br>structure. Refer to section 2.1.4.<br>This field is specified in logical blocks and is a 0’s based value. The AWUPF value shall be less<br>than or equal to the AWUN value.<br>If a write command is submitted that has a size less than or equal to the AWUPF value, the host<br>is guaranteed that the write is atomic to the NVM with respect to other read or write commands.<br>If a write command is submitted that is greater than this size, there is no guarantee of command<br>atomicity, but atomicity is guaranteed for portions of the command if the command is processed<br>in Multiple Atomicity Mode (refer to section 2.1.4.5). If the write size is less than or equal to the<br>AWUPF value and the write command fails, then subsequent read commands for the associated<br>logical blocks shall return data from the previous successful write command. If a write command<br>is submitted that has a size greater than the AWUPF value, then there is no guarantee of data<br>returned on subsequent reads of the associated logical blocks.|||
|…|||||||||

93

**Figure 117: Identify – Identify Controller data structure, NVM Command Set Specific Fields**

**Bytes**

**O/M1**

**Description**

533:532
O

**Atomic Compare & Write Unit (ACWU): This field indicates the size of the write operation**
guaranteed to be written atomically to the NVM across all namespaces with any supported
namespace format for a Compare and Write fused operation.
If a specific namespace guarantees a larger size than is reported in this field, then the Atomic
Compare & Write Unit size for that namespace is reported in the NACWU field in the Identify
Namespace data structure. Refer to section 2.1.4.
This field shall be supported if the Compare and Write fused command is supported. This field is
specified in logical blocks and is a 0’s based value. If a Compare and Write is submitted that
requests a transfer size larger than this value, then the controller may abort the command with a
status code of Atomic Write Unit Exceeded. If Compare and Write is not a supported fused
command, then this field shall be 0h.
…
Notes:
1.

**O/M definition: O = Optional, M = Mandatory**

**4.1.5.3**

**I/O Command Set Specific Identify Namespace Data Structure (CNS 05h)**
Figure 118 defines the I/O Command Set specific Identify Namespace data structure for the NVM
Command Set.
The Reported column in Figure 118 specifies fields in the I/O Command Set specific Identify Namespace
data structure for the NVM Command Set that define namespace capabilities used by a host to format or
create a namespace. If the NSID field is set to FFFFFFFFh, then the controller shall return an I/O Command
Set specific Identify Namespace data structure for the NVM Command Set that:
•
for fields in Figure 118 that indicate “Yes” in the Reported column, contain a value that is the same
for all namespaces using any of the LBA formats associated with the Number of LBA Formats field
(refer to section 5.5); and
•
for fields in Figure 118 that indicate “No” in the Reported column, contain a value cleared to 0h.
If the controller supports the Namespace Management capability (refer to the Namespace Management
section in the NVM Express Base Specification) and the NSID field is set to FFFFFFFFh, then the controller
shall return an I/O Command Set specific Identify Namespace data structure for the NVM Command Set.
If the controller does not support the Namespace Management capability and the NSID field is set to
FFFFFFFFh, then the controller may abort the command with a status code of Invalid Namespace or
Format.


||Bytes|||1<br>O/M|||Description||
|---|---|---|---|---|---|---|---|---|
|533:532|||O|||Atomic Compare & Write Unit (ACWU): This field indicates the size of the write operation<br>guaranteed to be written atomically to the NVM across all namespaces with any supported<br>namespace format for a Compare and Write fused operation.<br>If a specific namespace guarantees a larger size than is reported in this field, then the Atomic<br>Compare & Write Unit size for that namespace is reported in the NACWU field in the Identify<br>Namespace data structure. Refer to section 2.1.4.<br>This field shall be supported if the Compare and Write fused command is supported. This field is<br>specified in logical blocks and is a 0’s based value. If a Compare and Write is submitted that<br>requests a transfer size larger than this value, then the controller may abort the command with a<br>status code of Atomic Write Unit Exceeded. If Compare and Write is not a supported fused<br>command, then this field shall be 0h.|||
|…|||||||||
|Notes:<br>1. O/M definition: O = Optional, M = Mandatory|||||||||

94

**Figure 118: NVM Command Set I/O Command Set Specific Identify Namespace Data Structure**

**(CSI 00h)**

**Bytes**

**O/M1**

**Description**

**Reported2**

7:0
O

**Logical Block Storage Tag Mask (LBSTM): Indicates the mask for the Storage**
Tag field for the protection information (refer to section 5.3). The size of the mask
contained in this field is defined by the STS field (refer to Figure 119). If the size
of the mask contained in this field is less than 64 bits, the mask is contained in
the least-significant bits of this field. The host should ignore bits in this field that
are not part of the mask.
If end-to-end protection is not enabled in the namespace, then this field should
be ignored by the host.
If:
a)
the Qualified Protection Information Format Support bit is set to ‘1’; and
b)
the Storage Tag Masking Level Attribute field is set to a value of 010b
(i.e., Masking Not Supported);
or
a)
end-to-end protection is enabled;
b)
16b Guard Protection Information format is used; and
c)
the 16BPISTM bit is set to ‘1’ in the PIC field,
then each bit in the mask in this field shall be set to ‘1’.
If the Qualified Protection Information Format Support bit is set to ‘1’, then the
Storage Tag Masking Level Attribute field imposes constraints on how the bits

**in the mask contained in this field are allowed to be configured.**
No


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|7:0|||O|||Logical Block Storage Tag Mask (LBSTM): Indicates the mask for the Storage<br>Tag field for the protection information (refer to section 5.3). The size of the mask<br>contained in this field is defined by the STS field (refer to Figure 119). If the size<br>of the mask contained in this field is less than 64 bits, the mask is contained in<br>the least-significant bits of this field. The host should ignore bits in this field that<br>are not part of the mask.<br>If end-to-end protection is not enabled in the namespace, then this field should<br>be ignored by the host.<br>If:<br>a) the Qualified Protection Information Format Support bit is set to ‘1’; and<br>b) the Storage Tag Masking Level Attribute field is set to a value of 010b<br>(i.e., Masking Not Supported);<br>or<br>a) end-to-end protection is enabled;<br>b) 16b Guard Protection Information format is used; and<br>c) the 16BPISTM bit is set to ‘1’ in the PIC field,<br>then each bit in the mask in this field shall be set to ‘1’.<br>If the Qualified Protection Information Format Support bit is set to ‘1’, then the<br>Storage Tag Masking Level Attribute field imposes constraints on how the bits<br>in the mask contained in this field are allowed to be configured.|||No|||

95

**Figure 118: NVM Command Set I/O Command Set Specific Identify Namespace Data Structure**

**(CSI 00h)**

**Bytes**

**O/M1**

**Description**

**Reported2**

O

**Protection Information Capabilities (PIC): This field indicates the capabilities**
for the protection information formats.

**Bits**

**Description**
7:4
Reserved

**Qualified Protection Information Format Support (QPIFS): If**
this bit is set to ‘1’, then the namespace supports the Qualified
Protection Information Format field (refer to Figure 119) and the
Storage Tag Masking Level Attribute field. If this bit is cleared
to ‘0’, then the namespace does not support the Qualified
Protection Information Format field (refer to Figure 119) and
does not support the Storage Tag Masking Level Attribute field.

**Storage Tag Check Read Support (STCRS): If this bit is set**
to ‘1’, then the controller supports the Storage Tag Check Read
(STCR) bit in the Copy command (refer to Figure 34). If this bit
is cleared to ‘0’, the controller does not support the Storage Tag
Check Read bit in the Copy command. If the 16b Guard
Protection Information Storage Tag Support (PISTS16B) bit is
set to ‘1’, then this bit shall be set to ‘1’.

**16b Guard Protection Information Storage Tag Mask**

**(PISTM16B): If this bit is set to ‘1’, then the LBSTM field shall**
have all bits set to ‘1’ for the 16b Guard Protection Information.

**If this bit is cleared to ‘0’, then the Logical Block Storage Tag**
Mask field is allowed to have any bits set to ‘1’ for the 16b Guard
Protection Information.
If the PISTS16B bit is cleared to ‘0’, then the PISTM16B bit
should be ignored by the host.
If the Qualified Protection Information Format Support bit is set
to ‘1’, the PIF field is set to 11b (i.e., Qualified Type), and the
Storage Tag Masking Level Attribute is set to 010b (i.e.,
Masking Not Supported), then the PISTM16B bit shall be set to
‘1’.
The previous abbreviation for this bit was 16BPISTM.

**16b Guard Protection Information Storage Tag Support**

**(PISTS16B): If this bit is set to ‘1’, then the end-to-end**
protection 16b Guard Protection Information format (refer to
section 5.3.1.1) supports a non-zero value in the STS field. If
this bit is cleared to ‘0’, then the end-to-end protection 16b
Guard Protection Information format support requires that the
STS field be cleared to 0h (i.e., the Storage Tag field is not
supported).
If the 32b Guard Protection Information or 64b Guard Protection
Information is supported in any LBA format (refer to Figure 119),
then this bit shall be set to ‘1’.
The previous abbreviation for this bit was 16BPISTS.
Yes


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|8|||O|||Protection Information Capabilities (PIC): This field indicates the capabilities<br>for the protection information formats.<br>Bits Description<br>7:4 Reserved<br>Qualified Protection Information Format Support (QPIFS): If<br>this bit is set to ‘1’, then the namespace supports the Qualified<br>Protection Information Format field (refer to Figure 119) and the<br>3 Storage Tag Masking Level Attribute field. If this bit is cleared<br>to ‘0’, then the namespace does not support the Qualified<br>Protection Information Format field (refer to Figure 119) and<br>does not support the Storage Tag Masking Level Attribute field.<br>Storage Tag Check Read Support (STCRS): If this bit is set<br>to ‘1’, then the controller supports the Storage Tag Check Read<br>(STCR) bit in the Copy command (refer to Figure 34). If this bit<br>2 is cleared to ‘0’, the controller does not support the Storage Tag<br>Check Read bit in the Copy command. If the 16b Guard<br>Protection Information Storage Tag Support (PISTS16B) bit is<br>set to ‘1’, then this bit shall be set to ‘1’.<br>16b Guard Protection Information Storage Tag Mask<br>(PISTM16B): If this bit is set to ‘1’, then the LBSTM field shall<br>have all bits set to ‘1’ for the 16b Guard Protection Information.<br>If this bit is cleared to ‘0’, then the Logical Block Storage Tag<br>Mask field is allowed to have any bits set to ‘1’ for the 16b Guard<br>Protection Information.<br>If the PISTS16B bit is cleared to ‘0’, then the PISTM16B bit<br>1 should be ignored by the host.<br>If the Qualified Protection Information Format Support bit is set<br>to ‘1’, the PIF field is set to 11b (i.e., Qualified Type), and the<br>Storage Tag Masking Level Attribute is set to 010b (i.e.,<br>Masking Not Supported), then the PISTM16B bit shall be set to<br>‘1’.<br>The previous abbreviation for this bit was 16BPISTM.<br>16b Guard Protection Information Storage Tag Support<br>(PISTS16B): If this bit is set to ‘1’, then the end-to-end<br>protection 16b Guard Protection Information format (refer to<br>section 5.3.1.1) supports a non-zero value in the STS field. If<br>this bit is cleared to ‘0’, then the end-to-end protection 16b<br>Guard Protection Information format support requires that the<br>0 STS field be cleared to 0h (i.e., the Storage Tag field is not<br>supported).<br>If the 32b Guard Protection Information or 64b Guard Protection<br>Information is supported in any LBA format (refer to Figure 119),<br>then this bit shall be set to ‘1’.<br>The previous abbreviation for this bit was 16BPISTS.|||Yes|||


||Bits|||Description||
|---|---|---|---|---|---|
|7:4|||Reserved|||
|3|||Qualified Protection Information Format Support (QPIFS): If<br>this bit is set to ‘1’, then the namespace supports the Qualified<br>Protection Information Format field (refer to Figure 119) and the<br>Storage Tag Masking Level Attribute field. If this bit is cleared<br>to ‘0’, then the namespace does not support the Qualified<br>Protection Information Format field (refer to Figure 119) and<br>does not support the Storage Tag Masking Level Attribute field.|||
|2|||Storage Tag Check Read Support (STCRS): If this bit is set<br>to ‘1’, then the controller supports the Storage Tag Check Read<br>(STCR) bit in the Copy command (refer to Figure 34). If this bit<br>is cleared to ‘0’, the controller does not support the Storage Tag<br>Check Read bit in the Copy command. If the 16b Guard<br>Protection Information Storage Tag Support (PISTS16B) bit is<br>set to ‘1’, then this bit shall be set to ‘1’.|||
|1|||16b Guard Protection Information Storage Tag Mask<br>(PISTM16B): If this bit is set to ‘1’, then the LBSTM field shall<br>have all bits set to ‘1’ for the 16b Guard Protection Information.<br>If this bit is cleared to ‘0’, then the Logical Block Storage Tag<br>Mask field is allowed to have any bits set to ‘1’ for the 16b Guard<br>Protection Information.<br>If the PISTS16B bit is cleared to ‘0’, then the PISTM16B bit<br>should be ignored by the host.<br>If the Qualified Protection Information Format Support bit is set<br>to ‘1’, the PIF field is set to 11b (i.e., Qualified Type), and the<br>Storage Tag Masking Level Attribute is set to 010b (i.e.,<br>Masking Not Supported), then the PISTM16B bit shall be set to<br>‘1’.<br>The previous abbreviation for this bit was 16BPISTM.|||
|0|||16b Guard Protection Information Storage Tag Support<br>(PISTS16B): If this bit is set to ‘1’, then the end-to-end<br>protection 16b Guard Protection Information format (refer to<br>section 5.3.1.1) supports a non-zero value in the STS field. If<br>this bit is cleared to ‘0’, then the end-to-end protection 16b<br>Guard Protection Information format support requires that the<br>STS field be cleared to 0h (i.e., the Storage Tag field is not<br>supported).<br>If the 32b Guard Protection Information or 64b Guard Protection<br>Information is supported in any LBA format (refer to Figure 119),<br>then this bit shall be set to ‘1’.<br>The previous abbreviation for this bit was 16BPISTS.|||

96

**Figure 118: NVM Command Set I/O Command Set Specific Identify Namespace Data Structure**

**(CSI 00h)**

**Bytes**

**O/M1**

**Description**

**Reported2**

O

**Protection Information Format Attribute (PIFA): This field indicates attributes**
of the Protection Information Format supported by the namespace.

**Bits**

**Description**
7:3
Reserved

2:0

**Storage Tag Masking Level Attribute (STMLA): This field indicates**
the type of storage tag masking the namespace supports:

**Value**

**Definition**

000b

**Bit Granularity Masking: Unless otherwise**
specified, the bits in the Logical Block Storage
Tag Mask fields (refer to Figure 118 and Figure
125) may be any combination of ‘1’s and ‘0’s.

001b

**Byte Granularity Masking: The value of all bits**
within any individual byte in the Logical Block
Storage Tag Mask fields (refer to Figure 118 and
Figure 125) shall be the same, but that value may
differ from one byte to another, and the value of
all bits within any partial high-order byte that may
exist in the Logical Block Storage Tag Mask fields
shall be the same.

010b

**Masking Not Supported: Each bit in the Logical**
Block Storage Tag Mask field (refer to Figure 125)
is required to be set to ‘1’ when creating a
namespace using the Namespace Management

**command (refer to section 4.1.6).**
011b to 111b
Reserved
If the Qualified Protection Information Format Support bit (refer to
Figure 118) is cleared to ‘0’ or the PIF field is set to a value other than
11b (i.e., other than Qualified Type), then this field shall be cleared
to 000b.
Yes

11:10
Reserved

**Extended LBA Format (refer to section 5.5)**

15:12
O

**Extended LBA Format 0 Support (ELBAF0): This field indicates additional**
LBA Format 0 information related to the LBA Format 0 Support (LBAF0) field in
the Identify Namespace data structure. The Extended LBA format field is defined
in Figure 119.
Yes

19:16
O

**Extended LBA Format 1 Support (ELBAF1): This field indicates additional**
LBA Format 1 information related to the LBA Format 1 Support (LBAF1) field in
the Identify Namespace data structure. The Extended LBA format field is defined
in Figure 119.
Yes

…

267:264
O

**Extended LBA Format 63 Support (ELBAF63): This field indicates additional**
LBA Format 63 information related to the LBA Format 63 Support (LBAF63) field
in the Identify Namespace data structure. The Extended LBA format field is
defined in Figure 119.
Yes


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|9|||O|||Protection Information Format Attribute (PIFA): This field indicates attributes<br>of the Protection Information Format supported by the namespace.<br>Bits Description<br>7:3 Reserved<br>Storage Tag Masking Level Attribute (STMLA): This field indicates<br>the type of storage tag masking the namespace supports:<br>Value Definition<br>Bit Granularity Masking: Unless otherwise<br>specified, the bits in the Logical Block Storage<br>000b<br>Tag Mask fields (refer to Figure 118 and Figure<br>125) may be any combination of ‘1’s and ‘0’s.<br>Byte Granularity Masking: The value of all bits<br>within any individual byte in the Logical Block<br>Storage Tag Mask fields (refer to Figure 118 and<br>Figure 125) shall be the same, but that value may<br>001b<br>differ from one byte to another, and the value of<br>2:0 all bits within any partial high-order byte that may<br>exist in the Logical Block Storage Tag Mask fields<br>shall be the same.<br>Masking Not Supported: Each bit in the Logical<br>Block Storage Tag Mask field (refer to Figure 125)<br>010b is required to be set to ‘1’ when creating a<br>namespace using the Namespace Management<br>command (refer to section 4.1.6).<br>011b to 111b Reserved<br>If the Qualified Protection Information Format Support bit (refer to<br>Figure 118) is cleared to ‘0’ or the PIF field is set to a value other than<br>11b (i.e., other than Qualified Type), then this field shall be cleared<br>to 000b.|||Yes|||
|11:10||||||Reserved||||||
||Extended LBA Format (refer to section 5.5)|||||||||||
|15:12|||O|||Extended LBA Format 0 Support (ELBAF0): This field indicates additional<br>LBA Format 0 information related to the LBA Format 0 Support (LBAF0) field in<br>the Identify Namespace data structure. The Extended LBA format field is defined<br>in Figure 119.|||Yes|||
|19:16|||O|||Extended LBA Format 1 Support (ELBAF1): This field indicates additional<br>LBA Format 1 information related to the LBA Format 1 Support (LBAF1) field in<br>the Identify Namespace data structure. The Extended LBA format field is defined<br>in Figure 119.|||Yes|||
|…||||||||||||
|267:264|||O|||Extended LBA Format 63 Support (ELBAF63): This field indicates additional<br>LBA Format 63 information related to the LBA Format 63 Support (LBAF63) field<br>in the Identify Namespace data structure. The Extended LBA format field is<br>defined in Figure 119.|||Yes|||


||Bits|||Description||
|---|---|---|---|---|---|
|7:3|||Reserved|||
|2:0|||Storage Tag Masking Level Attribute (STMLA): This field indicates<br>the type of storage tag masking the namespace supports:<br>Value Definition<br>Bit Granularity Masking: Unless otherwise<br>specified, the bits in the Logical Block Storage<br>000b<br>Tag Mask fields (refer to Figure 118 and Figure<br>125) may be any combination of ‘1’s and ‘0’s.<br>Byte Granularity Masking: The value of all bits<br>within any individual byte in the Logical Block<br>Storage Tag Mask fields (refer to Figure 118 and<br>Figure 125) shall be the same, but that value may<br>001b<br>differ from one byte to another, and the value of<br>all bits within any partial high-order byte that may<br>exist in the Logical Block Storage Tag Mask fields<br>shall be the same.<br>Masking Not Supported: Each bit in the Logical<br>Block Storage Tag Mask field (refer to Figure 125)<br>010b is required to be set to ‘1’ when creating a<br>namespace using the Namespace Management<br>command (refer to section 4.1.6).<br>011b to 111b Reserved<br>If the Qualified Protection Information Format Support bit (refer to<br>Figure 118) is cleared to ‘0’ or the PIF field is set to a value other than<br>11b (i.e., other than Qualified Type), then this field shall be cleared<br>to 000b.|||


||Value|||Definition||
|---|---|---|---|---|---|
|000b|||Bit Granularity Masking: Unless otherwise<br>specified, the bits in the Logical Block Storage<br>Tag Mask fields (refer to Figure 118 and Figure<br>125) may be any combination of ‘1’s and ‘0’s.|||
|001b|||Byte Granularity Masking: The value of all bits<br>within any individual byte in the Logical Block<br>Storage Tag Mask fields (refer to Figure 118 and<br>Figure 125) shall be the same, but that value may<br>differ from one byte to another, and the value of<br>all bits within any partial high-order byte that may<br>exist in the Logical Block Storage Tag Mask fields<br>shall be the same.|||
|010b|||Masking Not Supported: Each bit in the Logical<br>Block Storage Tag Mask field (refer to Figure 125)<br>is required to be set to ‘1’ when creating a<br>namespace using the Namespace Management<br>command (refer to section 4.1.6).|||
|011b to 111b|||Reserved|||

97

**Figure 118: NVM Command Set I/O Command Set Specific Identify Namespace Data Structure**

**(CSI 00h)**

**Bytes**

**O/M1**

**Description**

**Reported2**

271:268
O

**Namespace Preferred Deallocate Granularity Large (NPDGL): This field**
indicates the recommended granularity in logical blocks for the Dataset
Management command with the Attribute – Deallocate bit set to ‘1’ in Command
Dword 11. If this field is not supported as defined by the OPTPERF field (refer
to Figure 114), then this field is reserved.
If this field is cleared to 0h, then this field does not indicate a recommended
granularity.
The value of this field may change if the namespace is reformatted.
If the Namespace Preferred Deallocate Alignment Large (NPDAL) field is
cleared to 0h, then the value of the NPDGL field should be a multiple of the
Namespace Preferred Deallocate Alignment (NPDA) field (refer to Figure 114).
If the Namespace Preferred Deallocate Alignment Large (NPDAL) field is
supported as defined by the OPTPERF field (refer to Figure 114) and is set to a
non-zero value, then the value of the NPDGL field should be a multiple of the
NPDAL field.
Refer to section 5.2.2 for how this field is utilized to improve performance and

**endurance.**
No

275:272
O

**Namespace Preferred Read Granularity (NPRG): This field is the smallest**
recommended read granularity in logical blocks for this namespace. This is a 0’s
based value. If this field is not supported as indicated by the OPTRPERF field,
then this field is reserved.
The size indicated by this field should be less than or equal to the size indicated
by the Maximum Data Transfer Size (MDTS) field (refer to the NVM Express
Base Specification) which is specified in units of minimum memory page size.
The value of this field may change if the namespace is reformatted. The size
should be a multiple of the Namespace Preferred Read Alignment (NPRA).
Refer to section 5.2.2 for how this field is utilized to improve performance.
No

279:276
O

**Namespace Preferred Read Alignment (NPRA): This field indicates the**
recommended read alignment in logical blocks for this namespace (refer to
section 5.2.2.3).
This is a 0’s based value. If this field is not supported as indicated by the
OPTRPERF field, then this field is reserved.
The value of this field may change if the namespace is reformatted.
Refer to section 5.2.2 for how this field is utilized to improve performance.
No

283:280
O

**Namespace Optimal Read Size (NORS): This field indicates the size in logical**
blocks for optimal read performance for this namespace. This is a 0’s based
value. If this field is not supported as indicated by the OPTRPERF field, then
this field is reserved.
The size indicated should be less than or equal to Maximum Data Transfer Size
(MDTS) that is specified in units of minimum memory page size. The value of
this field may change if the namespace is reformatted. The value of this field
should be a multiple of Namespace Preferred Read Granularity (NPRG).
Refer to section 5.2.2 for how this field is utilized to improve performance and
endurance.
No


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|271:268|||O|||Namespace Preferred Deallocate Granularity Large (NPDGL): This field<br>indicates the recommended granularity in logical blocks for the Dataset<br>Management command with the Attribute – Deallocate bit set to ‘1’ in Command<br>Dword 11. If this field is not supported as defined by the OPTPERF field (refer<br>to Figure 114), then this field is reserved.<br>If this field is cleared to 0h, then this field does not indicate a recommended<br>granularity.<br>The value of this field may change if the namespace is reformatted.<br>If the Namespace Preferred Deallocate Alignment Large (NPDAL) field is<br>cleared to 0h, then the value of the NPDGL field should be a multiple of the<br>Namespace Preferred Deallocate Alignment (NPDA) field (refer to Figure 114).<br>If the Namespace Preferred Deallocate Alignment Large (NPDAL) field is<br>supported as defined by the OPTPERF field (refer to Figure 114) and is set to a<br>non-zero value, then the value of the NPDGL field should be a multiple of the<br>NPDAL field.<br>Refer to section 5.2.2 for how this field is utilized to improve performance and<br>endurance.|||No|||
|275:272|||O|||Namespace Preferred Read Granularity (NPRG): This field is the smallest<br>recommended read granularity in logical blocks for this namespace. This is a 0’s<br>based value. If this field is not supported as indicated by the OPTRPERF field,<br>then this field is reserved.<br>The size indicated by this field should be less than or equal to the size indicated<br>by the Maximum Data Transfer Size (MDTS) field (refer to the NVM Express<br>Base Specification) which is specified in units of minimum memory page size.<br>The value of this field may change if the namespace is reformatted. The size<br>should be a multiple of the Namespace Preferred Read Alignment (NPRA).<br>Refer to section 5.2.2 for how this field is utilized to improve performance.|||No|||
|279:276|||O|||Namespace Preferred Read Alignment (NPRA): This field indicates the<br>recommended read alignment in logical blocks for this namespace (refer to<br>section 5.2.2.3).<br>This is a 0’s based value. If this field is not supported as indicated by the<br>OPTRPERF field, then this field is reserved.<br>The value of this field may change if the namespace is reformatted.<br>Refer to section 5.2.2 for how this field is utilized to improve performance.|||No|||
|283:280|||O|||Namespace Optimal Read Size (NORS): This field indicates the size in logical<br>blocks for optimal read performance for this namespace. This is a 0’s based<br>value. If this field is not supported as indicated by the OPTRPERF field, then<br>this field is reserved.<br>The size indicated should be less than or equal to Maximum Data Transfer Size<br>(MDTS) that is specified in units of minimum memory page size. The value of<br>this field may change if the namespace is reformatted. The value of this field<br>should be a multiple of Namespace Preferred Read Granularity (NPRG).<br>Refer to section 5.2.2 for how this field is utilized to improve performance and<br>endurance.|||No|||

98

**Figure 118: NVM Command Set I/O Command Set Specific Identify Namespace Data Structure**

**(CSI 00h)**

**Bytes**

**O/M1**

**Description**

**Reported2**

287:284
O

**Namespace Preferred Deallocate Alignment Large (NPDAL): This field**
indicates the recommended alignment in logical blocks for the Dataset
Management command with the Attribute – Deallocate bit set to ‘1’ in Dword 11.
If this field is not supported as indicated by the OPTPERF field, then this field is
reserved.
The value of this field may change if the namespace is reformatted.
Refer to section 5.2.2 for how this field is utilized to improve performance and
endurance.
No

291:288
O

**LBA Format Placement Shard Size (LBAPSS): This field indicates the optimal**
number of LBAs to be written to a Reclaim Group and then written to the other
Reclaim Groups in order to maximize I/O write performance.

**A value of 0h means that no Placement Shard Size value is reported.**
No

295:292
O

**Tracked LBA Allocation Granularity (TLBAAG): This field indicates the**
alignment and granularity, in logical blocks, for the reporting of allocated LBAs
for the namespace by the Get LBA Status command (refer to section 4.2.1). If
this field is cleared to the value of 0h, then the alignment and granularity are not
reported.
It is recommended that value of this field multiplied by the logical block data size
for this namespace be greater than or equal to 4 KiB.
Yes

4095:296
O
Reserved
Notes:
1.
O/M definition: O = Optional, M = Mandatory.
2.
Identifies fields that report information for the Identify command when querying the capabilities of LBA formats.

The Extended LBA format data structure is described in Figure 119.

**Figure 119: Extended LBA Format Data Structure, NVM Command Set Specific**

**Bits**

**Description**
31:13

**Reserved**

12:9

**Qualified Protection Information Format (QPIF):**
If:
a)
the Protection Information Format (PIF) field is set to a value of 11b (i.e., Qualified Type); and
b)
end-to-end protection information is enabled on a namespace formatted with this LBA format,
then
a)
this field indicates the protection information format (refer to section 5.3.1); and
b)
that protection information format is qualified by the Storage Tag Mask constraints, if any,
indicated by the Storage Tag Masking Level Attribute field (refer to Figure 118).
If the PIF field is set to a value other than 11b (i.e., Qualified Type) then this field is ignored.

**Value**

**Definition**
0h
16b Guard Protection Information
1h
32b Guard Protection Information
2h
64b Guard Protection Information
3h to Fh
Reserved


||Bytes|||1<br>O/M|||Description|||2<br>Reported||
|---|---|---|---|---|---|---|---|---|---|---|---|
|287:284|||O|||Namespace Preferred Deallocate Alignment Large (NPDAL): This field<br>indicates the recommended alignment in logical blocks for the Dataset<br>Management command with the Attribute – Deallocate bit set to ‘1’ in Dword 11.<br>If this field is not supported as indicated by the OPTPERF field, then this field is<br>reserved.<br>The value of this field may change if the namespace is reformatted.<br>Refer to section 5.2.2 for how this field is utilized to improve performance and<br>endurance.|||No|||
|291:288|||O|||LBA Format Placement Shard Size (LBAPSS): This field indicates the optimal<br>number of LBAs to be written to a Reclaim Group and then written to the other<br>Reclaim Groups in order to maximize I/O write performance.<br>A value of 0h means that no Placement Shard Size value is reported.|||No|||
|295:292|||O|||Tracked LBA Allocation Granularity (TLBAAG): This field indicates the<br>alignment and granularity, in logical blocks, for the reporting of allocated LBAs<br>for the namespace by the Get LBA Status command (refer to section 4.2.1). If<br>this field is cleared to the value of 0h, then the alignment and granularity are not<br>reported.<br>It is recommended that value of this field multiplied by the logical block data size<br>for this namespace be greater than or equal to 4 KiB.|||Yes|||
|4095:296|||O|||Reserved||||||
|Notes:<br>1. O/M definition: O = Optional, M = Mandatory.<br>2. Identifies fields that report information for the Identify command when querying the capabilities of LBA formats.||||||||||||


||Bits|||Description||
|---|---|---|---|---|---|
|31:13|||Reserved|||
|12:9|||Qualified Protection Information Format (QPIF):<br>If:<br>a) the Protection Information Format (PIF) field is set to a value of 11b (i.e., Qualified Type); and<br>b) end-to-end protection information is enabled on a namespace formatted with this LBA format,<br>then<br>a) this field indicates the protection information format (refer to section 5.3.1); and<br>b) that protection information format is qualified by the Storage Tag Mask constraints, if any,<br>indicated by the Storage Tag Masking Level Attribute field (refer to Figure 118).<br>If the PIF field is set to a value other than 11b (i.e., Qualified Type) then this field is ignored.<br>Value Definition<br>0h 16b Guard Protection Information<br>1h 32b Guard Protection Information<br>2h 64b Guard Protection Information<br>3h to Fh Reserved|||


||Value|||Definition||
|---|---|---|---|---|---|
|0h|||16b Guard Protection Information|||
|1h|||32b Guard Protection Information|||
|2h|||64b Guard Protection Information|||
|3h to Fh|||Reserved|||

99

**Figure 119: Extended LBA Format Data Structure, NVM Command Set Specific**

**Bits**

**Description**

8:7
Protection Information Format (PIF): This field indicates the protection information format (refer to
section 5.3.1) when end-to-end protection information is enabled on a namespace formatted with this
LBA format.
If:
•
end-to-end protection information is not supported by this LBA format; or
•
end-to-end protection is disabled on a namespace formatted with this LBA format,
then this field is undefined and should be ignored by the host.

**Value**

**Definition**
00b
16b Guard Protection Information
01b
32b Guard Protection Information
10b
64b Guard Protection Information

11b

**Qualified Type (QTYPE): If the Qualified Protection Information Format Support bit is set to**
‘1’, then the protection information format is as defined in the Qualified Protection Information
Format (QPIF) field. If the Qualified Protection Information Format Support bit is cleared to
‘0’, then this value shall not be used.

6:0
Storage Tag Size (STS): Identifies the number of most significant bits of the protection information
Storage and Reference Space field that define the Storage Tag field (refer to section 5.3.1.4).
This field does limit the minimum and maximum values allowed per protection information formats (refer
to section 5.3.1):

**Protection Information Format**

**Minimum Value**

**Maximum Value**
16b Guard Protection Information
32b Guard Protection Information
64b Guard Protection Information
If this field is cleared to 0h, then no bits of the Storage and Reference Space field are applied to the
Storage Tag field and therefore the Storage Tag field is not defined.
For the 16b Guard Protection, if this field is set to 32, then no bits of the Storage and Reference Space
field are applied to the Reference Tag field and therefore the Reference Tag field is not defined.
For the 64b Guard Protection, if this field is set to 48, then no bits of the Storage and Reference Space
field are applied to the Reference Tag field and therefore the Reference Tag field is not defined.

**4.1.5.4**

**I/O Command Set Specific Identify Controller Data Structure (CNS 06h, CSI 00h)**
Figure 120 defines the I/O Command Set specific Identify Controller data structure for the NVM Command
Set.


||Bits|||Description||
|---|---|---|---|---|---|
|8:7|||Protection Information Format (PIF): This field indicates the protection information format (refer to<br>section 5.3.1) when end-to-end protection information is enabled on a namespace formatted with this<br>LBA format.<br>If:<br>• end-to-end protection information is not supported by this LBA format; or<br>• end-to-end protection is disabled on a namespace formatted with this LBA format,<br>then this field is undefined and should be ignored by the host.<br>Value Definition<br>00b 16b Guard Protection Information<br>01b 32b Guard Protection Information<br>10b 64b Guard Protection Information<br>Qualified Type (QTYPE): If the Qualified Protection Information Format Support bit is set to<br>‘1’, then the protection information format is as defined in the Qualified Protection Information<br>11b<br>Format (QPIF) field. If the Qualified Protection Information Format Support bit is cleared to<br>‘0’, then this value shall not be used.|||
|6:0|||Storage Tag Size (STS): Identifies the number of most significant bits of the protection information<br>Storage and Reference Space field that define the Storage Tag field (refer to section 5.3.1.4).<br>This field does limit the minimum and maximum values allowed per protection information formats (refer<br>to section 5.3.1):<br>Protection Information Format Minimum Value Maximum Value<br>16b Guard Protection Information 0 32<br>32b Guard Protection Information 16 64<br>64b Guard Protection Information 0 48<br>If this field is cleared to 0h, then no bits of the Storage and Reference Space field are applied to the<br>Storage Tag field and therefore the Storage Tag field is not defined.<br>For the 16b Guard Protection, if this field is set to 32, then no bits of the Storage and Reference Space<br>field are applied to the Reference Tag field and therefore the Reference Tag field is not defined.<br>For the 64b Guard Protection, if this field is set to 48, then no bits of the Storage and Reference Space<br>field are applied to the Reference Tag field and therefore the Reference Tag field is not defined.|||


||Value|||Definition||
|---|---|---|---|---|---|
|00b|||16b Guard Protection Information|||
|01b|||32b Guard Protection Information|||
|10b|||64b Guard Protection Information|||
|11b|||Qualified Type (QTYPE): If the Qualified Protection Information Format Support bit is set to<br>‘1’, then the protection information format is as defined in the Qualified Protection Information<br>Format (QPIF) field. If the Qualified Protection Information Format Support bit is cleared to<br>‘0’, then this value shall not be used.|||


||Protection Information Format|||Minimum Value|||Maximum Value||
|---|---|---|---|---|---|---|---|---|
|16b Guard Protection Information|||0|||32|||
|32b Guard Protection Information|||16|||64|||
|64b Guard Protection Information|||0|||48|||

100

**Figure 120: I/O Command Set Specific Identify Controller Data Structure for the NVM Command Set**

**Bytes**

**O/M1**

**Description**

**O**

**Verify Size Limit (VSL): If the Verify Support (NVMVFYS) bit is set to ‘1’ in the Optional**
NVM Command Support (ONCS) field in the Identify Controller data structure (refer to the
Identify Controller data structure (CNS 01h) section in the NVM Express Base Specification),
then:
a)
a non-zero value in this field indicates the recommended maximum data size for a
Verify command (refer to section 3.3.5); and
b)
a value of 0h in this field indicates that no recommended maximum data size for a
Verify command is reported.
If the NVMVFYS bit is cleared to ‘0’, then:
a)
a non-zero value in this field indicates that the controller supports the Verify
command with the maximum data size limit indicated by this field (refer to section
3.3.5); and
b)
a value of 0h in this field indicates that the controller does not support the Verify
command.
The non-zero value is in units of the minimum memory page size (CAP.MPSMIN) and is
reported as a power of two (2^n).
If the MEM bit is cleared to ‘0’ in the CTRATT field in the Identify Controller data structure,
then this field includes the length of metadata, if metadata is interleaved with the logical block
data.

**If the MEM bit is set to ‘1’, then this field excludes the length of metadata.**

**O**

**Write Zeroes Size Limit (WZSL): If the Write Zeroes Support Variants (NVMWZSV) bit is**
set to ‘1’ in the Optional NVM Command Support (ONCS) field, then:
a)
a non-zero value in this field indicates the recommended maximum data size for a
Write Zeroes command (refer to section 3.3.8); and
b)
a value of 0h in this field indicates that no recommended maximum data size for a
Write Zeroes command is reported.
If the NVMWZSV bit is cleared to ‘0’, then:
a)
a non-zero value in this field indicates that the controller supports the Write Zeroes
command with the maximum data size limit indicated by this field (refer to section
3.3.8); and
b)
a value of 0h in this field indicates that the controller does not support the Write
Zeroes command.
If the MAXWZD bit in the ONCS field is set to ‘1’, then the controller supports a larger
maximum data size for Write Zeroes commands with the Deallocate bit set to ‘1’ than the
controller supports for Write Zeroes commands that have the Deallocate bit cleared to ‘0’,
and the controller shall:
•
set this field to a non-zero maximum data size value that applies to Write Zeroes
commands with the Deallocate bit cleared to ‘0’; and
•
set the Write Zeroes with Deallocate Size Limit (WZDSL) field to a larger non-zero
maximum data size value that applies to Write Zeroes commands with the
Deallocate bit set to ‘1’.
The non-zero value is in units of the minimum memory page size (CAP.MPSMIN) and is
reported as a power of two (2^n).
If the MEM bit is cleared to ‘0’ in the CTRATT field in the Identify Controller data structure,
then this field includes the length of metadata, if metadata is interleaved with the logical block
data.

**If the MEM bit is set to ‘1’, then this field excludes the length of metadata.**


||Bytes|||1<br>O/M|||Description||
|---|---|---|---|---|---|---|---|---|
|00|||O|||Verify Size Limit (VSL): If the Verify Support (NVMVFYS) bit is set to ‘1’ in the Optional<br>NVM Command Support (ONCS) field in the Identify Controller data structure (refer to the<br>Identify Controller data structure (CNS 01h) section in the NVM Express Base Specification),<br>then:<br>a) a non-zero value in this field indicates the recommended maximum data size for a<br>Verify command (refer to section 3.3.5); and<br>b) a value of 0h in this field indicates that no recommended maximum data size for a<br>Verify command is reported.<br>If the NVMVFYS bit is cleared to ‘0’, then:<br>a) a non-zero value in this field indicates that the controller supports the Verify<br>command with the maximum data size limit indicated by this field (refer to section<br>3.3.5); and<br>b) a value of 0h in this field indicates that the controller does not support the Verify<br>command.<br>The non-zero value is in units of the minimum memory page size (CAP.MPSMIN) and is<br>reported as a power of two (2^n).<br>If the MEM bit is cleared to ‘0’ in the CTRATT field in the Identify Controller data structure,<br>then this field includes the length of metadata, if metadata is interleaved with the logical block<br>data.<br>If the MEM bit is set to ‘1’, then this field excludes the length of metadata.|||
|01|||O|||Write Zeroes Size Limit (WZSL): If the Write Zeroes Support Variants (NVMWZSV) bit is<br>set to ‘1’ in the Optional NVM Command Support (ONCS) field, then:<br>a) a non-zero value in this field indicates the recommended maximum data size for a<br>Write Zeroes command (refer to section 3.3.8); and<br>b) a value of 0h in this field indicates that no recommended maximum data size for a<br>Write Zeroes command is reported.<br>If the NVMWZSV bit is cleared to ‘0’, then:<br>a) a non-zero value in this field indicates that the controller supports the Write Zeroes<br>command with the maximum data size limit indicated by this field (refer to section<br>3.3.8); and<br>b) a value of 0h in this field indicates that the controller does not support the Write<br>Zeroes command.<br>If the MAXWZD bit in the ONCS field is set to ‘1’, then the controller supports a larger<br>maximum data size for Write Zeroes commands with the Deallocate bit set to ‘1’ than the<br>controller supports for Write Zeroes commands that have the Deallocate bit cleared to ‘0’,<br>and the controller shall:<br>• set this field to a non-zero maximum data size value that applies to Write Zeroes<br>commands with the Deallocate bit cleared to ‘0’; and<br>• set the Write Zeroes with Deallocate Size Limit (WZDSL) field to a larger non-zero<br>maximum data size value that applies to Write Zeroes commands with the<br>Deallocate bit set to ‘1’.<br>The non-zero value is in units of the minimum memory page size (CAP.MPSMIN) and is<br>reported as a power of two (2^n).<br>If the MEM bit is cleared to ‘0’ in the CTRATT field in the Identify Controller data structure,<br>then this field includes the length of metadata, if metadata is interleaved with the logical block<br>data.<br>If the MEM bit is set to ‘1’, then this field excludes the length of metadata.|||

101

**O**

**Write Uncorrectable Size Limit (WUSL): If the Write Uncorrectable Support Variants**
(NVMWUSV) bit is set to ‘1’ in the Optional NVM Command Support (ONCS) field, then:
a)
a non-zero value in this field indicates the recommended maximum data size for a
Write Uncorrectable command (refer to section 3.3.7); and
b)
a value of 0h in this field indicates that no recommended maximum data size for a
Write Uncorrectable command is reported.
If the NVMWUSV bit in the ONCS field is cleared to ‘0’, then:
a)
a non-zero value in this field indicates that the controller supports the Write
Uncorrectable command with the maximum data size limit indicated by this field
(refer to section 3.3.7); and
b)
a value of 0h in this field indicates that the controller does not support the Write
Uncorrectable command.
The non-zero value is in units of the minimum memory page size (CAP.MPSMIN) and is
reported as a power of two (2^n).
If the MEM bit is cleared to ‘0’ in the CTRATT field in the Identify Controller data structure,
then this field includes the length of metadata, if metadata is interleaved with the logical block
data.

**If the MEM bit is set to ‘1’, then this field excludes the length of metadata.**

**O**

**Dataset Management Ranges Limit (DMRL): If the Dataset Management Support Variants**
(NVMDSMSV) bit is set to ‘1’ in the Optional NVM Command Support (ONCS) field, then:
a)
a non-zero value in this field indicates the recommended maximum number of
logical block ranges for a Dataset Management command (refer to section 3.3.3);
and
b)
a value of 0h in this field indicates that no recommended maximum number of
logical block ranges for a Dataset Management command is reported.
If the NVMDSMSV bit in the ONCS field is cleared to ‘0’, then:
a)
a non-zero value in this field indicates that the controller supports the Dataset
Management command with the maximum number of logical block ranges limit
indicated by this field (refer to section 3.3.3); and
b)
a value of 0h in this field indicates that the controller does not support the Dataset

**Management command.**

**07:04**

**O**

**Dataset Management Range Size Limit (DMRSL): If the Dataset Management Support**
Variants (NVMDSMSV) bit is set to ‘1’ in the Optional NVM Command Support (ONCS) field,
then:
a)
a non-zero value in this field indicates the recommended maximum number of
logical blocks in a single range for a Dataset Management command (refer to
section 3.3.3); and
b)
a value of 0h in this field indicates that no recommended maximum number of
logical blocks in a single range for a Dataset Management command is reported.
If the NVMDSMSV bit in the ONCS field is cleared to ‘0’, then:
a)
a non-zero value in this field indicates that the controller supports the Dataset
Management command with the maximum number of logical blocks in a single
range limit indicated by this field (refer to section 3.3.3); and
b)
a value of 0h in this field indicates that the controller does not support the Dataset

**Management command.**


|02|O|Write Uncorrectable Size Limit (WUSL): If the Write Uncorrectable Support Variants<br>(NVMWUSV) bit is set to ‘1’ in the Optional NVM Command Support (ONCS) field, then:<br>a) a non-zero value in this field indicates the recommended maximum data size for a<br>Write Uncorrectable command (refer to section 3.3.7); and<br>b) a value of 0h in this field indicates that no recommended maximum data size for a<br>Write Uncorrectable command is reported.<br>If the NVMWUSV bit in the ONCS field is cleared to ‘0’, then:<br>a) a non-zero value in this field indicates that the controller supports the Write<br>Uncorrectable command with the maximum data size limit indicated by this field<br>(refer to section 3.3.7); and<br>b) a value of 0h in this field indicates that the controller does not support the Write<br>Uncorrectable command.<br>The non-zero value is in units of the minimum memory page size (CAP.MPSMIN) and is<br>reported as a power of two (2^n).<br>If the MEM bit is cleared to ‘0’ in the CTRATT field in the Identify Controller data structure,<br>then this field includes the length of metadata, if metadata is interleaved with the logical block<br>data.<br>If the MEM bit is set to ‘1’, then this field excludes the length of metadata.|
|---|---|---|
|03|O|Dataset Management Ranges Limit (DMRL): If the Dataset Management Support Variants<br>(NVMDSMSV) bit is set to ‘1’ in the Optional NVM Command Support (ONCS) field, then:<br>a) a non-zero value in this field indicates the recommended maximum number of<br>logical block ranges for a Dataset Management command (refer to section 3.3.3);<br>and<br>b) a value of 0h in this field indicates that no recommended maximum number of<br>logical block ranges for a Dataset Management command is reported.<br>If the NVMDSMSV bit in the ONCS field is cleared to ‘0’, then:<br>a) a non-zero value in this field indicates that the controller supports the Dataset<br>Management command with the maximum number of logical block ranges limit<br>indicated by this field (refer to section 3.3.3); and<br>b) a value of 0h in this field indicates that the controller does not support the Dataset<br>Management command.|
|07:04|O|Dataset Management Range Size Limit (DMRSL): If the Dataset Management Support<br>Variants (NVMDSMSV) bit is set to ‘1’ in the Optional NVM Command Support (ONCS) field,<br>then:<br>a) a non-zero value in this field indicates the recommended maximum number of<br>logical blocks in a single range for a Dataset Management command (refer to<br>section 3.3.3); and<br>b) a value of 0h in this field indicates that no recommended maximum number of<br>logical blocks in a single range for a Dataset Management command is reported.<br>If the NVMDSMSV bit in the ONCS field is cleared to ‘0’, then:<br>a) a non-zero value in this field indicates that the controller supports the Dataset<br>Management command with the maximum number of logical blocks in a single<br>range limit indicated by this field (refer to section 3.3.3); and<br>b) a value of 0h in this field indicates that the controller does not support the Dataset<br>Management command.|

102

**15:08**

**O**

**Dataset Management Size Limit (DMSL): If the Dataset Management Support Variants**
(NVMDSMSV) bit is set to ‘1’ in the Optional NVM Command Support (ONCS) field, then:
a)
a non-zero value in this field indicates the recommended maximum total number of
logical blocks for a Dataset Management command (refer to section 3.3.3); and
b)
a value of 0h in this field indicates that no recommended maximum total number of
logical blocks for a Dataset Management command is reported.
If the NVMDSMSV bit in the ONCS field is cleared to ‘0’, then:
a)
a non-zero value in this field indicates that the controller supports the Dataset
Management command with the maximum total number of logical blocks limit
indicated by this field (refer to section 3.3.3); and
b)
a value of 0h in this field indicates that the controller does not support the Dataset

**Management command.**

O

**Key Per I/O Capabilities (KPIOCAP): This field indicates the attributes for Key Per I/O**
capability (refer to section 5.4).

**Bits**

**Description**
7:2
Reserved

**Key Per I/O Scope (KPIOSC): If this bit is set to ‘1’, then the Key Per I/O**
capability applies to all namespaces in the NVM subsystem when Key Per I/O
capability is enabled. If this bit is cleared to ‘0’, then the Key Per I/O capability
does not apply to all namespaces in the NVM subsystem and is allowed to be
independently enabled and disabled uniquely on each namespace within the
NVM subsystem.

**Key Per I/O Supported (KPIOS): If this bit is set to ‘1’, then the controller**
supports the Key Per I/O capability. If this bit is cleared to ‘0’, then the controller
does not support the Key Per I/O capability.

O

**Write Zeroes With Deallocate Size Limit (WZDSL): A non-zero value in this field indicates**
the maximum data size for Write Zeroes commands with the Deallocate bit set to '1'. A 0h
value in this field indicates that the maximum data size for Write Zeroes commands does not
depend on the value of the Deallocate bit.
For Write Zeroes commands with the Deallocate bit cleared to ‘0’, this field has no effect
(refer to the WZSL field).
For Write Zeroes commands with the Deallocate bit set to ‘1’, if this field is set to a non-zero
value, then:
a)
if the Write Zeroes Support Variants (NVMWZSV) bit in the ONCS field is set to ‘1’,
then the value in this field is the recommended maximum data size and the value
in the WZSL field is not used; and
b)
if the NVMWZSV bit is cleared to ‘0’, then the value in this field is the maximum
data size limit and the value in the WZSL field is not used.
If the WZSL field is cleared to 0h, then this field shall be cleared to 0h. If the WZSL field is
not cleared to 0h, then the value of this field shall either be 0h or greater than the value in
the WZSL field.
The non-zero value is in units of the minimum memory page size (CAP.MPSMIN) and is
reported as a power of two (2^n).
If the MEM bit is cleared to ‘0’ in the CTRATT field in the Identify Controller data structure,
then this field includes the length of metadata, if metadata is interleaved with the logical block
data.
If the MEM bit is set to ‘1’, then this field excludes the length of metadata.


|15:08|O|Dataset Management Size Limit (DMSL): If the Dataset Management Support Variants<br>(NVMDSMSV) bit is set to ‘1’ in the Optional NVM Command Support (ONCS) field, then:<br>a) a non-zero value in this field indicates the recommended maximum total number of<br>logical blocks for a Dataset Management command (refer to section 3.3.3); and<br>b) a value of 0h in this field indicates that no recommended maximum total number of<br>logical blocks for a Dataset Management command is reported.<br>If the NVMDSMSV bit in the ONCS field is cleared to ‘0’, then:<br>a) a non-zero value in this field indicates that the controller supports the Dataset<br>Management command with the maximum total number of logical blocks limit<br>indicated by this field (refer to section 3.3.3); and<br>b) a value of 0h in this field indicates that the controller does not support the Dataset<br>Management command.|
|---|---|---|
|16|O|Key Per I/O Capabilities (KPIOCAP): This field indicates the attributes for Key Per I/O<br>capability (refer to section 5.4).<br>Bits Description<br>7:2 Reserved<br>Key Per I/O Scope (KPIOSC): If this bit is set to ‘1’, then the Key Per I/O<br>capability applies to all namespaces in the NVM subsystem when Key Per I/O<br>capability is enabled. If this bit is cleared to ‘0’, then the Key Per I/O capability<br>1<br>does not apply to all namespaces in the NVM subsystem and is allowed to be<br>independently enabled and disabled uniquely on each namespace within the<br>NVM subsystem.<br>Key Per I/O Supported (KPIOS): If this bit is set to ‘1’, then the controller<br>0 supports the Key Per I/O capability. If this bit is cleared to ‘0’, then the controller<br>does not support the Key Per I/O capability.|
|17|O|Write Zeroes With Deallocate Size Limit (WZDSL): A non-zero value in this field indicates<br>the maximum data size for Write Zeroes commands with the Deallocate bit set to '1'. A 0h<br>value in this field indicates that the maximum data size for Write Zeroes commands does not<br>depend on the value of the Deallocate bit.<br>For Write Zeroes commands with the Deallocate bit cleared to ‘0’, this field has no effect<br>(refer to the WZSL field).<br>For Write Zeroes commands with the Deallocate bit set to ‘1’, if this field is set to a non-zero<br>value, then:<br>a) if the Write Zeroes Support Variants (NVMWZSV) bit in the ONCS field is set to ‘1’,<br>then the value in this field is the recommended maximum data size and the value<br>in the WZSL field is not used; and<br>b) if the NVMWZSV bit is cleared to ‘0’, then the value in this field is the maximum<br>data size limit and the value in the WZSL field is not used.<br>If the WZSL field is cleared to 0h, then this field shall be cleared to 0h. If the WZSL field is<br>not cleared to 0h, then the value of this field shall either be 0h or greater than the value in<br>the WZSL field.<br>The non-zero value is in units of the minimum memory page size (CAP.MPSMIN) and is<br>reported as a power of two (2^n).<br>If the MEM bit is cleared to ‘0’ in the CTRATT field in the Identify Controller data structure,<br>then this field includes the length of metadata, if metadata is interleaved with the logical block<br>data.<br>If the MEM bit is set to ‘1’, then this field excludes the length of metadata.|


||Bits|||Description||
|---|---|---|---|---|---|
|7:2|||Reserved|||
|1|||Key Per I/O Scope (KPIOSC): If this bit is set to ‘1’, then the Key Per I/O<br>capability applies to all namespaces in the NVM subsystem when Key Per I/O<br>capability is enabled. If this bit is cleared to ‘0’, then the Key Per I/O capability<br>does not apply to all namespaces in the NVM subsystem and is allowed to be<br>independently enabled and disabled uniquely on each namespace within the<br>NVM subsystem.|||
|0|||Key Per I/O Supported (KPIOS): If this bit is set to ‘1’, then the controller<br>supports the Key Per I/O capability. If this bit is cleared to ‘0’, then the controller<br>does not support the Key Per I/O capability.|||

103
19:18
M

**Admin Optional Command Support (AOCS): This field indicates the optional Admin**
commands and features supported by the controller.

**Bits**

**Description**
15:01
Reserved

**Reporting Allocated LBA Supported (RALBAS): If this bit is set to ‘1’, then**
the controller supports the Get LBA Status capability with the Action Type
value of 02h (refer to section 4.2.1). If this bit is cleared to ‘0’, then the
controller does not support the Get LBA Status capability with the Action
Type value of 02h.

23:20
M

**Version (VER): This field contains a Specification Version Descriptor (refer to the NVM**
Express Base Specification) indicating the version of this specification supported by the
controller, as defined in Figure 121.

O

**LBA Migration Queue Format (LBAMQF): This field indicates the format supported by this**
controller for User Data Migration Queue entries. Refer to section 5.6.

**Value**

**Definition**

**Reference**
0h

**LBA Migration Queue Entry Type 0.**
Figure 177
1h to BFh
Reserved
C0h to FFh
Vendor Specific
4095:25
M
Reserved
Notes:
1.
O/M definition: O = Optional, M = Mandatory.


|19:18|M|Admin Optional Command Support (AOCS): This field indicates the optional Admin<br>commands and features supported by the controller.<br>Bits Description<br>15:01 Reserved<br>Reporting Allocated LBA Supported (RALBAS): If this bit is set to ‘1’, then<br>the controller supports the Get LBA Status capability with the Action Type<br>00 value of 02h (refer to section 4.2.1). If this bit is cleared to ‘0’, then the<br>controller does not support the Get LBA Status capability with the Action<br>Type value of 02h.|
|---|---|---|
|23:20|M|Version (VER): This field contains a Specification Version Descriptor (refer to the NVM<br>Express Base Specification) indicating the version of this specification supported by the<br>controller, as defined in Figure 121.|
|24|O|LBA Migration Queue Format (LBAMQF): This field indicates the format supported by this<br>controller for User Data Migration Queue entries. Refer to section 5.6.<br>Value Definition Reference<br>0h LBA Migration Queue Entry Type 0. Figure 177<br>1h to BFh Reserved<br>C0h to FFh Vendor Specific|
|4095:25|M|Reserved|
|Notes:<br>1. O/M definition: O = Optional, M = Mandatory.|||


||Bits||Description||
|---|---|---|---|---|
|15:01|||Reserved||
|00|||Reporting Allocated LBA Supported (RALBAS): If this bit is set to ‘1’, then<br>the controller supports the Get LBA Status capability with the Action Type<br>value of 02h (refer to section 4.2.1). If this bit is cleared to ‘0’, then the<br>controller does not support the Get LBA Status capability with the Action<br>Type value of 02h.||


|Value|||Definition|||Reference||
|---|---|---|---|---|---|---|---|
|0h||LBA Migration Queue Entry Type 0.|||Figure 177|||
|1h to BFh||Reserved||||||
|C0h to FFh||Vendor Specific||||||

104
Published versions of this specification and the values that shall be reported by compliant controllers are
defined in Figure 121.

**Figure 121: NVM Command Set Specification Version Descriptor Field Values**

**Specification Versions 1**

**MJR Field**

**MNR Field**

**TER Field**
1.0
1h
0h
0h
1.1
1h
1h
0h
1.2
1h
2h
0h
Notes:
1.
The specification version listed includes lettered versions (e.g., 1.0 includes 1.0, 1.0a, 1.0b, etc.).

**4.1.5.5**

**NVM Command Set Identify Namespace Data Structure (CNS 09h, CSI 00h)**
An NVM Command Set Identify Namespace data structure (refer to Figure 114) is returned to the host for
the Format Index specified by the CNS Specific Identifier field as defined in Figure 122. The returned NVM
Command Set Identify Namespace data structure specifies fields that define capabilities used by a host to
format or create a namespace. If the specified Format Index is valid (refer to section 5.5), then the controller
shall return an NVM Command Set Identify Namespace data structure that:
•
for fields in Figure 114 that indicate “Yes” in the Reported column, contain a value that is the same
for all namespaces using the specified Format Index; and
•
for fields in Figure 114 that indicate “No” in the Reported column, contain a value cleared to 0h.

**Figure 122: Command Dword 11 - CNS Specific Identifiers**

**Bits**

**Description**
15:0

**Format Index (FIDX): This field specifies the Format Index identifying the LBA Format for which**
capabilities are to be returned. Refer to section 5.5.

**4.1.5.6**

**Identify I/O Command Set specific Namespace data structure (CNS 0Ah, CSI 00h)**
An I/O Command Set specific Identify Namespace data structure for the NVM Command Set (refer to Figure
118) is returned to the host for the Format Index specified by the CNS Specific Identifier field as defined in
Figure 122. The returned I/O Command Set specific Identify Namespace data structure for the NVM
Command Set specifies fields that define capabilities used by a host to format or create a namespace. If
the specified Format Index is valid (refer to section 5.5), then the controller shall return an I/O Command
Set specific Identify Namespace data structure for the NVM Command Set that:
•
for fields in Figure 118 that indicate “Yes” in the Reported column, contain a value that is the same
for all namespaces using the specified Format Index; and
•
for fields in Figure 118 that indicate “No” in the Reported column, contain a value cleared to 0h.

**4.1.5.7**

**Identify Namespace data structure for an Allocated Namespace ID (CNS 11h)**
An Identify Namespace data structure (refer to Figure 114) is returned to the host for the specified
namespace if the value in the Namespace Identifier (NSID) field is an allocated NSID. If the value in the
NSID field specifies an unallocated NSID, then the controller returns a zero filled data structure.
If the value in the NSID field specifies an invalid NSID, then the controller shall abort the command with a
status code of Invalid Namespace or Format. If the NSID field is set to FFFFFFFFh, then the controller shall
abort the command with a status code of Invalid Namespace or Format.


||1<br>Specification Versions|||MJR Field|||MNR Field|||TER Field||
|---|---|---|---|---|---|---|---|---|---|---|---|
|1.0|||1h|||0h|||0h|||
|1.1|||1h|||1h|||0h|||
|1.2|||1h|||2h|||0h|||
|Notes:<br>1. The specification version listed includes lettered versions (e.g., 1.0 includes 1.0, 1.0a, 1.0b, etc.).||||||||||||


||Bits|||Description||
|---|---|---|---|---|---|
|15:0|||Format Index (FIDX): This field specifies the Format Index identifying the LBA Format for which<br>capabilities are to be returned. Refer to section 5.5.|||

105

**4.1.5.8**

**Namespace Granularity List (CNS 16h)**
If the controller supports reporting of Namespace Granularity (refer to section5.7), then a Namespace
Granularity List (refer to Figure 123) is returned to the host for up to:
a) 16 namespace granularity descriptors (refer to Figure 124) if the LBA Format Extension Enable
(LBAFEE) field is cleared to 0h in the Host Behavior Support feature (refer to the Host Behavior
Support section in the NVM Express Base Specification); or
b) 64 namespace granularity descriptors if the LBAFEE field is set to 1h in the Host Behavior Support
feature.

**Figure 123: Namespace Granularity List**

**Bytes**

**Description**

**Header**

03:00

**Namespace Granularity Attributes (NGA): This field indicates attributes of the Namespace**
Granularity List.

**Bits**

**Description**
31:1
Reserved

**Granularity Descriptor Mapping (GDM): If this bit is set to ‘1’, then each valid namespace**
granularity descriptor applies to the LBA format having the same Format Index and the
Number of Descriptors field shall be equal to the sum of the values represented by the
Number of LBA Formats field and the Number of Unique Attribute LBA Formats field in the
Identify Namespace data structure (refer to Figure 114 and section 5.5). If this bit is cleared
to ‘0’, then NG Descriptor 0 shall apply to all LBA formats and the Number of Descriptors
field shall be cleared to 0h.

**Number of Descriptors (ND): This field indicates the number of valid namespace granularity**
descriptors in the list. This is a 0’s based value.
The namespace granularity descriptors with an index greater than the value in this field shall be
cleared to 0h.
31:05
Reserved

**Namespace Granularity Descriptor List**

47:32

**NG Descriptor 0 (NGD0): This field contains the first namespace granularity descriptor in the list.**
This namespace granularity descriptor applies to LBA formats as indicated by the Granularity
Descriptor Mapping bit.
63:48
NG Descriptor 1 (NGD1): This field contains the second namespace granularity descriptor in the list.

**This namespace granularity descriptor applies to LBA Format 1.**
…
…
1055:1040
NG Descriptor 63 (NGD63): This field contains the last namespace granularity descriptor in the list.

**This namespace granularity descriptor applies to LBA Format 63.**

The format of the namespace granularity descriptor is defined in Figure 124.

**Figure 124: Namespace Granularity Descriptor**

**Bytes**

**Description**

07:00
Namespace Size Granularity (NSG): Indicates the preferred granularity of allocation of namespace size
when a namespace is created. The value is in bytes. A value of 0h indicates that the namespace size
granularity is not reported.

15:08
Namespace Capacity Granularity (NCG): Indicates the preferred granularity of allocation of namespace
capacity when a namespace is created. The value is in bytes. A value of 0h indicates that the namespace
capacity granularity is not reported.


||Bytes|||Description||
|---|---|---|---|---|---|
||Header|||||
|03:00|||Namespace Granularity Attributes (NGA): This field indicates attributes of the Namespace<br>Granularity List.<br>Bits Description<br>31:1 Reserved<br>Granularity Descriptor Mapping (GDM): If this bit is set to ‘1’, then each valid namespace<br>granularity descriptor applies to the LBA format having the same Format Index and the<br>Number of Descriptors field shall be equal to the sum of the values represented by the<br>0 Number of LBA Formats field and the Number of Unique Attribute LBA Formats field in the<br>Identify Namespace data structure (refer to Figure 114 and section 5.5). If this bit is cleared<br>to ‘0’, then NG Descriptor 0 shall apply to all LBA formats and the Number of Descriptors<br>field shall be cleared to 0h.|||
|04|||Number of Descriptors (ND): This field indicates the number of valid namespace granularity<br>descriptors in the list. This is a 0’s based value.<br>The namespace granularity descriptors with an index greater than the value in this field shall be<br>cleared to 0h.|||
|31:05|||Reserved|||
||Namespace Granularity Descriptor List|||||
|47:32|||NG Descriptor 0 (NGD0): This field contains the first namespace granularity descriptor in the list.<br>This namespace granularity descriptor applies to LBA formats as indicated by the Granularity<br>Descriptor Mapping bit.|||
|63:48|||NG Descriptor 1 (NGD1): This field contains the second namespace granularity descriptor in the list.<br>This namespace granularity descriptor applies to LBA Format 1.|||
|…|||…|||
|1055:1040|||NG Descriptor 63 (NGD63): This field contains the last namespace granularity descriptor in the list.<br>This namespace granularity descriptor applies to LBA Format 63.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:1|||Reserved|||
|0|||Granularity Descriptor Mapping (GDM): If this bit is set to ‘1’, then each valid namespace<br>granularity descriptor applies to the LBA format having the same Format Index and the<br>Number of Descriptors field shall be equal to the sum of the values represented by the<br>Number of LBA Formats field and the Number of Unique Attribute LBA Formats field in the<br>Identify Namespace data structure (refer to Figure 114 and section 5.5). If this bit is cleared<br>to ‘0’, then NG Descriptor 0 shall apply to all LBA formats and the Number of Descriptors<br>field shall be cleared to 0h.|||


||Bytes|||Description||
|---|---|---|---|---|---|
|07:00|||Namespace Size Granularity (NSG): Indicates the preferred granularity of allocation of namespace size<br>when a namespace is created. The value is in bytes. A value of 0h indicates that the namespace size<br>granularity is not reported.|||
|15:08|||Namespace Capacity Granularity (NCG): Indicates the preferred granularity of allocation of namespace<br>capacity when a namespace is created. The value is in bytes. A value of 0h indicates that the namespace<br>capacity granularity is not reported.|||

106

**4.1.5.9**

**I/O Command Set specific Identify Namespace data structure for an Allocated Namespace**

**ID (CNS 1Bh)**
An I/O Command Set specific Identify Namespace data structure for the NVM Command Set (refer to Figure
118) is returned to the host for the namespace specified by the value in the NSID field if the specified NSID
is an allocated NSID. If the specified NSID is not an allocated NSID (e.g., unallocated NSID or invalid NSID),
then the controller behaves as specified in the NVM Express Base Specification.


**4.1.5.10 Command Set Index Usage for the NVM Command Set**
The following sections provide an example on how a host uses the CSI value of 00h for accessing Identify
Namespace data structures for a namespace associated with the NVM Command Set.


**4.1.5.10.1 Determining the Identify Command Information Associated with a Namespace**
For a host to determine the Identify Namespace data structures (refer to section 1.4.2.4) for a namespace
associated with the NVM Command Set, the host is required to issue the following Identify commands in
any order:
a) An Identify command with:
a. the CNS field set to 08h; and
b. the NSID field set to the NSID of the namespace,
to access the I/O Command Set Independent Identify Namespace data structure (refer to the NVM
Express Base Specification);
b) An identify command with:
a. the CNS field set to 00h; and
b. the NSID field set to the NSID of the namespace,
to access the Identify Namespace data structure (refer to section 4.1.5.1);
c) An Identify command with:
a. the CNS field set to 05h;
b. the CSI field set to 00h; and
c. the NSID field set to the NSID of the zoned namespace,
to access the I/O Command Set specific Identify Namespace data structure for the NVM Command
Set (refer to section 4.1.5.3).


**4.1.5.10.2 Determining the Identify Command Information Associated with a Format Index**
For a host to determine the Identify Namespace data structures associated with a specific Format Index
(i.e., determining information about a namespace associated with the NVM Command Set prior to creating
that namespace), the host is required to issue the following Identify commands in any order:
a) An Identify command with:
a. the CNS field set to 08h; and
b. the NSID field set to FFFFFFFFh,
to access the I/O Command Set Independent Identify Namespace data structure (refer to the NVM
Express Base Specification);
b) An Identify command with:
a. The CNS field set to 09h;
107
b. The CSI field set to 00h;
c. The NSID field set to 0h; and
d. The CNS Specific Identifier field set to the Format Index,
to access the Identify Namespace data structure (refer to section 4.1.5.5); and
c) An Identify command with:
a. the CNS set to OAh;
b. the CSI set to 00h;
c. the NSID field set to 0h; and
d. the CNS Specific Identifier field set to the Format Index,
to access the I/O Command Set specific Identify Namespace data structure for the NVM Command
Set (refer to section 4.1.5.6).

**Namespace Management command**
The Namespace Management command operates as defined in the NVM Express Base Specification.
The host specified namespace management fields are specific to the I/O Command Set. The data structure
passed to the create operation for the NVM Command Set (CSI 00h) is defined in Figure 125. Fields that
are reserved should be cleared to 0h by the host. After successful completion of a Namespace Management
command with the create operation, the namespace is formatted with the specified attributes.
If the LBA Format Extension Enable (LBAFEE) field is not set to 1h in the Host Behavior Support feature
(refer to the Host Behavior Support section in the NVM Express Base Specification), then a controller aborts
a Namespace Management command with a status code of Invalid Namespace or Format that specifies to
create a namespace that is formatted with (refer to section 5.3.1):
a) 16b Guard Protection Information with the STS field set to a non-zero value;
b) 32b Guard Protection Information; or
c) 64b Guard Protection Information.
Implementations may impose requirements on which bits are allowed to be masked in the Logical Block
Storage Tag Mask field (refer to Figure 125). Those requirements are defined in the LBSTM field in Figure
118 and the Storage Tag Masking Level Attribute field in Figure 118. If any of the requirements specified in
those two fields are not met, then the controller shall abort the command with a status code of Invalid Field
in Command.
If Flexible Data Placement (refer to the NVM Express Base Specification) is enabled in the specified
Endurance Group and the Select field is set to Create (i.e., 0h):
•
The Placement Handle List allows the host to specify the Reclaim Unit Handle associated with each
specified Placement Handle. The number of Placement Handles in the list is specified by the
NPHNDLS field which is limited to a value less than or equal to the lesser value of:
o
the number of Reclaim Unit Handles supported by the FDP configuration (refer to the NVM
Express Base Specification); and
o
128.
•
If the NPHNDLS field is cleared to 0h, then:
o
if no namespace exists that was created with a Namespace Management command that
specified the NPHNDLS field cleared to 0h in the specified Endurance Group, then the
controller shall select a Reclaim Unit Handle for the Placement Handle 0 Associated RUH
108
field that is not utilized by any namespace in the same Endurance Group that was created
with a Namespace Management command that specified a non-zero NPHNDLS field; and
o
if any namespace exists that was created with a Namespace Management command that
specified the NPHNDLS field cleared to 0h in the specified Endurance Group, then the
controller shall utilize the same Reclaim Unit Handle for the Placement Handle 0
Associated RUH field that is utilized by those namespaces in the same Endurance Group
that were created with a Namespace Management command that specified the NPHNDLS
field cleared to 0h.
•
If:
o
the NPHNDLS field is cleared to 0h; and
o
all Reclaim Unit Handle Identifiers accessible to the namespace are allocated to
namespaces created by Namespace Management command with the NPHNDLS field set
to a non-zero value,
then the controller shall abort the command with a status code of Invalid Placement Handle List.
•
If:
o
the NPHNDLS field is non-zero; and
o
a Reclaim Unit Handle Identifier specified by the host is the same as the Reclaim Unit
Handle Identifier selected by the controller due to an existing namespace being created by
Namespace Management command with the NPHNDLS field cleared to 0h,
then the controller shall abort the command with a status code of Invalid Placement Handle List.
•
If the NPHNDLS field is greater than the lesser value of:
o
the number of Reclaim Unit Handles supported by the FDP configuration (refer to the NVM
Express Base Specification); and
o
128,
then the controller shall abort the command with a status code of Invalid Placement Handle List.
•
If a Reclaim Unit Handle Identifier value in any entry in the Placement Handle List is greater than
or equal to the number of Reclaim Unit Handles supported by the FDP configuration for the
Endurance Group (refer to the NVM Express Base Specification), then controller shall abort the
command with a status code of Invalid Placement Handle List.
•
If the same Reclaim Unit Handle Identifier value is in two or more entries in the Placement Handle
List, then controller shall abort the command with a status code of Invalid Placement Handle List.
•
Namespaces that exist in the specified Endurance Group that utilize the same (i.e., share) Reclaim
Unit Handle shall have the same user data format (i.e., report the same Format Index). If a Reclaim
Unit Handle specified in the Placement Handle List is utilized by another namespace and the
Format Index for that namespace does not match the specified Format Index for the namespace to
be created, then the controller shall abort the command with a status code of Invalid Format.

**Figure 125: Namespace Management – Host Specified Fields**

**Bytes**

**Description**

**Host Specified**

**Fields that are a subset of the Identify Namespace data structure (refer to Figure 114)**
07:00

**Namespace Size (NSZE)**
Yes
15:08

**Namespace Capacity (NCAP)**
Yes
25:16
Reserved

**Formatted LBA Size (FLBAS)**
Yes


||Bytes|||Description|||Host Specified||
|---|---|---|---|---|---|---|---|---|
||Fields that are a subset of the Identify Namespace data structure (refer to Figure 114)||||||||
|07:00|||Namespace Size (NSZE)|||Yes|||
|15:08|||Namespace Capacity (NCAP)|||Yes|||
|25:16|||Reserved||||||
|26|||Formatted LBA Size (FLBAS)|||Yes|||

109

**Figure 125: Namespace Management – Host Specified Fields**

**Bytes**

**Description**

**Host Specified**
28:27
Reserved

**End-to-end Data Protection Type Settings (DPS)**
Yes

**Namespace Multi-path I/O and Namespace Sharing Capabilities (NMIC)**
Yes
91:31
Reserved
95:92

**ANA Group Identifier (ANAGRPID) 1**
Yes
99:96
Reserved
101:100

**NVM Set Identifier (NVMSETID) 1, 3**
Yes
103:102

**Endurance Group Identifier (ENDGID) 1**
Yes
383:104
Reserved

**Fields that are not a subset of the Identify Namespace data structure.**
391:384

**Logical Block Storage Tag Mask (LBSTM)**
Yes

393:392

**Number of Placement Handles 2 (NPHNDLS): This field specifies the number of**
Placement Handles included in the Placement Handle List.
If the Flexible Data Placement capability (refer to the NVM Express Base
Specification) is not supported or not enabled in specified Endurance Group, then
the controller shall ignore this field.
Yes

498:394
Reserved
511:499
Reserved for I/O Command Sets that extend this specification. Refer to the applicable NVM Express
I/O Command Set specification (e.g., NVM Express Zoned Namespace Command Set Specification).

**Placement Handle List**

513:512

**Placement Handle 0 Associated RUH2: This field specifies the Reclaim Unit**
Handle Identifier to be associated with the Placement Handle value 0h, if any.
This Reclaim Unit Handle Identifier is used by the controller for any write commands
that do not specify the Data Placement Directive.
If the Flexible Data Placement capability (refer to the NVM Express Base
Specification) is not supported or not enabled in specified Endurance Group, then
the controller shall ignore this field.
Yes

515:514

**Placement Handle 1 Associated RUH2: This field specifies the Reclaim Unit**
Handle Identifier to be associated with the Placement Handle value 1h, if any.
If the Flexible Data Placement capability (refer to the NVM Express Base
Specification) is not supported or not enabled in specified Endurance Group, then
the controller shall ignore this field.
Yes

…

767:766

**Placement Handle 127 Associated RUH2: This field specifies the Reclaim Unit**
Handle Identifier to be associated with the Placement Handle value 127, if any.
If the Flexible Data Placement capability (refer to the NVM Express Base
Specification) is not supported or not enabled in specified Endurance Group, then
the controller shall ignore this field.
Yes

4096:768
Reserved
Notes:
1.
A value of 0h specifies that the controller determines the value to use (refer to the Namespace Management
section of the NVM Express Base Specification). If the associated feature is not supported, then this field is
ignored by the controller.
2.
Refer to the Flexible Data Placement section in the NVM Express Base Specification for requirements and use
of this field. These fields are reserved if Flexible Data Placement is disabled in the specified Endurance Group.
3.
NVM Sets are not supported if FDP is enabled in the specified Endurance Group as defined in the NVM Express
Base Specification.


||Bytes|||Description|||Host Specified||
|---|---|---|---|---|---|---|---|---|
|28:27|||Reserved||||||
|29|||End-to-end Data Protection Type Settings (DPS)|||Yes|||
|30|||Namespace Multi-path I/O and Namespace Sharing Capabilities (NMIC)|||Yes|||
|91:31|||Reserved||||||
|95:92|||1<br>ANA Group Identifier (ANAGRPID)|||Yes|||
|99:96|||Reserved||||||
|101:100|||1, 3<br>NVM Set Identifier (NVMSETID)|||Yes|||
|103:102|||1<br>Endurance Group Identifier (ENDGID)|||Yes|||
|383:104|||Reserved||||||
||Fields that are not a subset of the Identify Namespace data structure.||||||||
|391:384|||Logical Block Storage Tag Mask (LBSTM)|||Yes|||
|393:392|||2<br>Number of Placement Handles (NPHNDLS): This field specifies the number of<br>Placement Handles included in the Placement Handle List.<br>If the Flexible Data Placement capability (refer to the NVM Express Base<br>Specification) is not supported or not enabled in specified Endurance Group, then<br>the controller shall ignore this field.|||Yes|||
|498:394|||Reserved||||||
|511:499|||Reserved for I/O Command Sets that extend this specification. Refer to the applicable NVM Express<br>I/O Command Set specification (e.g., NVM Express Zoned Namespace Command Set Specification).||||||
||Placement Handle List||||||||
|513:512|||2<br>Placement Handle 0 Associated RUH : This field specifies the Reclaim Unit<br>Handle Identifier to be associated with the Placement Handle value 0h, if any.<br>This Reclaim Unit Handle Identifier is used by the controller for any write commands<br>that do not specify the Data Placement Directive.<br>If the Flexible Data Placement capability (refer to the NVM Express Base<br>Specification) is not supported or not enabled in specified Endurance Group, then<br>the controller shall ignore this field.|||Yes|||
|515:514|||2<br>Placement Handle 1 Associated RUH : This field specifies the Reclaim Unit<br>Handle Identifier to be associated with the Placement Handle value 1h, if any.<br>If the Flexible Data Placement capability (refer to the NVM Express Base<br>Specification) is not supported or not enabled in specified Endurance Group, then<br>the controller shall ignore this field.|||Yes|||
|…|||||||||
|767:766|||2<br>Placement Handle 127 Associated RUH : This field specifies the Reclaim Unit<br>Handle Identifier to be associated with the Placement Handle value 127, if any.<br>If the Flexible Data Placement capability (refer to the NVM Express Base<br>Specification) is not supported or not enabled in specified Endurance Group, then<br>the controller shall ignore this field.|||Yes|||
|4096:768|||Reserved||||||
|Notes:<br>1. A value of 0h specifies that the controller determines the value to use (refer to the Namespace Management<br>section of the NVM Express Base Specification). If the associated feature is not supported, then this field is<br>ignored by the controller.<br>2. Refer to the Flexible Data Placement section in the NVM Express Base Specification for requirements and use<br>of this field. These fields are reserved if Flexible Data Placement is disabled in the specified Endurance Group.<br>3. NVM Sets are not supported if FDP is enabled in the specified Endurance Group as defined in the NVM Express<br>Base Specification.|||||||||

110

**Sanitize command**
The Sanitize command operates as defined in the NVM Express Base Specification.
In addition to the requirements in the NVM Express Base Specification, the following NVM Command Set
Admin commands (refer to Figure 126) are allowed while a sanitize operation is in progress:

**Figure 126: Sanitize Operations – Admin Commands Allowed**

**Admin Command**

**Additional Restrictions**

Get Log Page
The log pages listed below are allowed in addition to the log pages listed in the NVM Express
Base Specification.

**Log Pages**

**Additional Restrictions**
Error Information
Return zeroes in the User Data field.

**Track Send command**
Upon posting the successful completion to a Track Send command (refer the NVM Express Base
Specification) that specifies:
•
the Log User Data Changes management operation;
•
the Logging Action (LACT) bit set to ‘1’; and
•
a Controller Data Queue Identifier for a created LBA Migration Queue,
then the controller shall post entries into that LBA Migration Queue that identifies the logical block
modifications to the attached namespaces on the controller associated with the LBA Migration Queue (refer
to section 5.6). Posting of these entries into the LBA Migration Queue continues until the logging is stopped
as specified by the NVM Express Base specification.
If the Reporting Allocated LBA Supported (RALBAS) bit is set to ‘1’ (refer to Figure 120), then after that
Track Send command completes successfully, any logical block modifications to the attached namespaces
on the controller associated with the LBA Migration Queue (refer to section 5.6) that occur during the
processing of that Track Send command are reported by a Get LBA Status command with the Action Type
field set to 02h (i.e., Return Allocated LBAs). Those logical block modifications to the attached namespaces
on the controller associated with the LBA Migration Queue (refer to section 5.6) that occur during the
processing of that Track Send command may also be logged into the LBA Migration Queue.
If the RALBAS bit is cleared to ‘0’, then after that Track Send command completes successfully, any logical
block modifications to the attached namespaces on the controller associated with the LBA Migration Queue
(refer to section 5.6) that occur during the processing of that Track Send command may be logged into the
LBA Migration Queue.
The posting of an entry into the LBA Migration Queue as a result of a Track Send command to indicate:
•
the start of logging user data changes; or
•
the stop of logging user data changes,
is not required to be posted prior to posting the completion of that Track Send command.
If:
•
the specified LBA Migration Queue in Track Send command with the Log User Data Changes
management operation and the Logging Action (LACT) bit set to ‘1’; and
•
that specified LBA Migration Queue is currently full,
then the controller may abort the command with a status code of Controller Data Queue Full.


||Admin Command|||Additional Restrictions||
|---|---|---|---|---|---|
|Get Log Page|||The log pages listed below are allowed in addition to the log pages listed in the NVM Express<br>Base Specification.<br>Log Pages Additional Restrictions<br>Error Information Return zeroes in the User Data field.|||


||Log Pages|||Additional Restrictions||
|---|---|---|---|---|---|
|Error Information|||Return zeroes in the User Data field.|||

111
If the Track Send command is successful and there is a pending Controller Data Queue Full Error event for
the LBA Migration Queue specified by the CDQID field, then the controller shall discard that pending event
with no effects to the state of the LBA Migration Queue.

**4.2**

**I/O Command Set Specific Admin commands**

In addition to the I/O Command Set Specific Admin commands defined in the NVM Express Base
Specification, the NVM Command Set defines the Admin commands defined in this section.

**Get LBA Status command**
The Get LBA Status command requests information about LBAs (refer to section 5.2.1). If the Get LBA
Status command completes successfully, then the LBA Status Descriptor List, defined in Figure 131, is
returned in the data buffer for that command.
The Get LBA Status command uses the Data Pointer, Command Dword 10, Command Dword 11,
Command Dword 12, and Command Dword 13 fields. All other command specific fields are reserved.
The Maximum Number of Dwords (MNDW) field contains the maximum number of dwords to return. Upon
successful command completion, the actual amount of data returned by the controller is indicated by the
Number of LBA Status Descriptors (NLSD) field in the LBA Status Descriptor List.

**Figure 127: Get LBA Status – Data Pointer**

**Bits**

**Description**
127:00

**Data Pointer (DPTR): This field specifies the start of the data buffer. Refer to the Common Command**
Format figure in the NVM Express Base Specification for the definition of this field.

**Figure 128: Get LBA Status – Command Dword 10 and Command Dword 11**

**Bits**

**Description**
63:00
Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block addressed by this
command. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits 63:32.

**Figure 129: Get LBA Status – Command Dword 12**

**Bits**

**Description**
31:00

**Maximum Number of Dwords (MNDW): This field specifies the maximum number of dwords to return.**
This is a 0’s based value.

**Figure 130: Get LBA Status – Command Dword 13**

**Bits**

**Description**

31:24

**Action Type (ATYPE): This field specifies the mechanism the controller uses in determining the LBA**
Status Descriptors to return as defined in Figure 132.

**Value**

**M/O/P1**

**Definition**

**Reference**

**Section**
02h
O
Return tracked allocated LBAs in the specified range
4.2.1.1.1
10h
O
Perform a scan and return Untracked LBAs and Tracked
LBAs in the specified range
4.2.1.1.2
11h
O
Return Tracked LBAs in the specified range
All others
Reserved
Notes:
1.
O = Optional, M = Mandatory, P = Prohibited


||Bits|||Description||
|---|---|---|---|---|---|
|127:00|||Data Pointer (DPTR): This field specifies the start of the data buffer. Refer to the Common Command<br>Format figure in the NVM Express Base Specification for the definition of this field.|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:00|||Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block addressed by this<br>command. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits 63:32.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:00|||Maximum Number of Dwords (MNDW): This field specifies the maximum number of dwords to return.<br>This is a 0’s based value.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:24|||Action Type (ATYPE): This field specifies the mechanism the controller uses in determining the LBA<br>Status Descriptors to return as defined in Figure 132.<br>1 Reference<br>Value M/O/P Definition<br>Section<br>02h O Return tracked allocated LBAs in the specified range 4.2.1.1.1<br>Perform a scan and return Untracked LBAs and Tracked<br>10h O<br>LBAs in the specified range 4.2.1.1.2<br>11h O Return Tracked LBAs in the specified range<br>All others Reserved<br>Notes:<br>1. O = Optional, M = Mandatory, P = Prohibited|||
|||||||


|Value|1<br>M/O/P|Definition||Reference||
|---|---|---|---|---|---|
|||||Section||
|02h|O|Return tracked allocated LBAs in the specified range|4.2.1.1.1|||
|10h|O|Perform a scan and return Untracked LBAs and Tracked<br>LBAs in the specified range|4.2.1.1.2|||
|11h|O|Return Tracked LBAs in the specified range||||
|All others||Reserved||||
|Notes:<br>1. O = Optional, M = Mandatory, P = Prohibited||||||

112

**Figure 130: Get LBA Status – Command Dword 13**

**Bits**

**Description**
23:16
Reserved

15:00
Range Length (RL): This field specifies the length of the range of contiguous LBAs, beginning at Starting
LBA (SLBA), that the action specified in the Action Type (ATYPE) field shall be performed on. A value of
0h in this field specifies the length of a range beginning at Starting LBA and ending at Namespace Size
(NSZE) minus 1 (refer to Figure 114).

**4.2.1.1**

**Get LBA Status Action Type Mechanisms**

**4.2.1.1.1**

**Return Allocated LBAs (Action Type 02h)**
The Get LBA Status command specifying an Action Type of 02h requests information about allocated LBAs.
The controller shall return information about allocated LBAs in the range specified in the Get LBA Status
command for the namespace specified in the NSID field. A controller is allowed to track the Allocated LBAs
on the alignment and granularity specified by the Tracked LBA Allocation Granularity (TLBAAG) field in the
I/O Command Set specific Identify Namespace data structure for the NVM Command Set (refer to Figure
118).
If all the logical blocks within the same alignment and granularity unit are deallocated, then all LBAs in that
granularity and alignment unit that are in the LBA range specified in the Get LBA Status command shall not
be reported as being allocated in the returned information for the Get LBA Status command.
If all of the logical blocks within the same alignment and granularity unit are allocated, then all LBAs in that
granularity and alignment unit that are in the LBA range specified in the Get LBA Status command shall be
reported as being allocated in the returned information for the Get LBA Status command as being allocated.
If within the same alignment and granularity unit:
•
one or more logical blocks are not deallocated; and
•
one or more logical blocks are deallocated,
then all LBAs in that granularity and alignment unit that are in the LBA range specified in the Get LBA Status
command shall be reported as being allocated in the returned information for the Get LBA Status command
as being allocated.

**4.2.1.1.2**

**Potentially Unrecoverable LBAs (Action Type 10h and 11h)**
A Get LBA Status command specifying an Action Type of 10h or 11h requests information about Potentially
Unrecoverable LBAs.
A controller identifies Potentially Unrecoverable LBAs using the following two report types:

**a) Tracked LBAs: a list of Potentially Unrecoverable LBAs associated with physical storage. These**
may be discovered through a background scan where the controller examines the media in the
background or discovered through other means. The Tracked LBA list is able to be returned without
significant delay; or

**b) Untracked LBAs: a list of Potentially Unrecoverable LBAs generated by a scan originated by a**
Get LBA Status command with the ATYPE field set to 10h. The controller scans internal data
structures related to the specified range of LBAs to determine which LBAs are Potentially
Unrecoverable LBAs. The controller may use this scan to determine which LBAs in which
namespaces are affected by a component (e.g., die or channel) failure. Significant delays may be
incurred during the processing of a Get LBA Status command with the ATYPE field set to 10h. After


||Bits|||Description||
|---|---|---|---|---|---|
|23:16|||Reserved|||
|15:00|||Range Length (RL): This field specifies the length of the range of contiguous LBAs, beginning at Starting<br>LBA (SLBA), that the action specified in the Action Type (ATYPE) field shall be performed on. A value of<br>0h in this field specifies the length of a range beginning at Starting LBA and ending at Namespace Size<br>(NSZE) minus 1 (refer to Figure 114).|||

113
the controller discovers Untracked LBAs, those LBAs may or may not be added to the list of Tracked
LBAs.
If the value in the Action Type (ATYPE) field is set to 10h, then:
a) the controller shall generate a list of Untracked LBAs as described in this section;
b) the controller shall return Untracked LBAs and Tracked LBAs in the range specified in the Get LBA
Status command for the specified namespace;
c) the controller shall remove all LBAs in the range specified in the Get LBA Status command, which
prior to processing the Get LBA Status command were successfully re-written, from relevant
internal data structures (e.g., internal Tracked LBA list);
d) the controller shall ensure that any such successfully re-written logical blocks are not reported in
any LBA Status Descriptor Entries returned by the Get LBA Status command unless, after having
been removed from relevant internal data structures and prior to processing the Get LBA Status
command, those LBAs were newly detected as being Potentially Unrecoverable LBAs; and
e) the list of Untracked LBAs returned by the Get LBA Status command may be discarded by the
controller or added to the Tracked LBA list once the command has completed.
If the value in the Action Type (ATYPE) field is set to 11h, then the controller shall:
a) return Tracked LBAs in the range specified in the Get LBA Status command for the specified
namespace;
b) remove all LBAs in the range specified in the Get LBA Status command, which prior to processing
the Get LBA Status command were successfully re-written, from relevant internal data structures
(e.g., internal Tracked LBA list);
c) ensure that any such successfully re-written logical blocks are not reported in any LBA Status
Descriptor Entries returned by the Get LBA Status command unless, after having been removed
from relevant internal data structures and prior to processing the Get LBA Status command, those
LBAs were newly detected as being Potentially Unrecoverable LBAs; and
d) not perform a foreground scan to generate and return Untracked LBAs.
In response to a Get LBA Status command, the controller returns LBA Status Descriptors that describe
LBAs written by a Write Uncorrectable command in addition to any other LBAs that may return an
Unrecovered Read Error status discovered through other mechanisms. The list of Tracked LBAs and the
list of Untracked LBAs may be included in LBA Status Descriptor Entries that describe LBAs written by a
Write Uncorrectable command. If an LBA Status Descriptor Entry describes only LBAs written by a Write
Uncorrectable command, then the LBA Range Status (LBARS) field in the Status field should be set to
011b in that entry.

**4.2.1.2**

**LBA Status Descriptor List**
Figure 131 defines the LBA Status Descriptor List returned in the data buffer.

**Figure 131: LBA Status Descriptor List**

**Bytes**

**Description**

**Header**

03:00

**Number of LBA Status Descriptors (NLSD): This field indicates the number of LBA Status**
Descriptor Entries returned by the controller in this data structure. A value of 0h in this field
indicates that no LBA Status Descriptor Entry list is returned.


||Bytes|||Description||
|---|---|---|---|---|---|
||Header|||||
|03:00|||Number of LBA Status Descriptors (NLSD): This field indicates the number of LBA Status<br>Descriptor Entries returned by the controller in this data structure. A value of 0h in this field<br>indicates that no LBA Status Descriptor Entry list is returned.|||

114

**Figure 131: LBA Status Descriptor List**

**Bytes**

**Description**

**Completion Condition (CMPC): This field indicates the condition that caused completion of the**
Get LBA Status command.

**Value**

**Definition**
0h
No indication of the completion condition.

1h

**INCOMPLETE: The command completed as a result of transferring the number**
of Dwords specified in the MNDW field and:
•
for any ATYPE, additional LBA Status Descriptor Entries are available to
transfer that are associated with the specified LBA range; or
•
for ATYPE set to 10h, the scan did not complete.

2h

**COMPLETE: The command completed as a result of completing the action**
specified in the Action Type field over the number of logical blocks specified in the
Range Length field and there are no additional LBA Status Descriptor Entries
available to transfer that are associated with the specified range.
All others
Reserved
07:05
Reserved

**LBA Status Descriptor Entry List**
23:08

**LBA Status Descriptor Entry 0: This field contains the first LBA Status Descriptor Entry in the**
list, if present.
39:24

**LBA Status Descriptor Entry 1: This field contains the second LBA Status Descriptor Entry in**

**the list, if present.**
…

**…**
(NLSD*16+23):
(NLSD*16+8)

**LBA Status Descriptor Entry NLSD-1: This field contains the last LBA Status Descriptor Entry**

**in the list, if present.**

**Figure 132: LBA Status Descriptor Entry**

**Bytes**

**Description**
07:00
Descriptor Starting LBA (DSLBA): This field indicates the 64-bit address of the first logical block of
the LBA range for which this LBA Status Descriptor Entry reports LBA status.

11:08

**Number of Logical Blocks (NLB): This field indicates the number of contiguous logical blocks**
reported in this LBA Status Descriptor Entry. The controller should perform the action specified in the
Action Type field in such a way that the value in this field reports the largest number of contiguous
logical blocks possible (i.e., multiple consecutive LBA Status Descriptor Entries should not report
contiguous LBAs that span those entries, but rather, LBA Status Descriptor Entries should be
consolidated into the fewest number of LBA Status Descriptor Entries possible). This is a 0’s based
value.
Reserved


||Bytes|||Description||
|---|---|---|---|---|---|
|04|||Completion Condition (CMPC): This field indicates the condition that caused completion of the<br>Get LBA Status command.<br>Value Definition<br>0h No indication of the completion condition.<br>INCOMPLETE: The command completed as a result of transferring the number<br>of Dwords specified in the MNDW field and:<br>1h • for any ATYPE, additional LBA Status Descriptor Entries are available to<br>transfer that are associated with the specified LBA range; or<br>• for ATYPE set to 10h, the scan did not complete.<br>COMPLETE: The command completed as a result of completing the action<br>specified in the Action Type field over the number of logical blocks specified in the<br>2h<br>Range Length field and there are no additional LBA Status Descriptor Entries<br>available to transfer that are associated with the specified range.<br>All others Reserved|||
|07:05|||Reserved|||
||LBA Status Descriptor Entry List|||||
|23:08|||LBA Status Descriptor Entry 0: This field contains the first LBA Status Descriptor Entry in the<br>list, if present.|||
|39:24|||LBA Status Descriptor Entry 1: This field contains the second LBA Status Descriptor Entry in<br>the list, if present.|||
|…|||…|||
|(NLSD*16+23):<br>(NLSD*16+8)|||LBA Status Descriptor Entry NLSD-1: This field contains the last LBA Status Descriptor Entry<br>in the list, if present.|||


||Value|||Definition||
|---|---|---|---|---|---|
|0h|||No indication of the completion condition.|||
|1h|||INCOMPLETE: The command completed as a result of transferring the number<br>of Dwords specified in the MNDW field and:<br>• for any ATYPE, additional LBA Status Descriptor Entries are available to<br>transfer that are associated with the specified LBA range; or<br>• for ATYPE set to 10h, the scan did not complete.|||
|2h|||COMPLETE: The command completed as a result of completing the action<br>specified in the Action Type field over the number of logical blocks specified in the<br>Range Length field and there are no additional LBA Status Descriptor Entries<br>available to transfer that are associated with the specified range.|||
|All others|||Reserved|||


||Bytes|||Description||
|---|---|---|---|---|---|
|07:00|||Descriptor Starting LBA (DSLBA): This field indicates the 64-bit address of the first logical block of<br>the LBA range for which this LBA Status Descriptor Entry reports LBA status.|||
|11:08|||Number of Logical Blocks (NLB): This field indicates the number of contiguous logical blocks<br>reported in this LBA Status Descriptor Entry. The controller should perform the action specified in the<br>Action Type field in such a way that the value in this field reports the largest number of contiguous<br>logical blocks possible (i.e., multiple consecutive LBA Status Descriptor Entries should not report<br>contiguous LBAs that span those entries, but rather, LBA Status Descriptor Entries should be<br>consolidated into the fewest number of LBA Status Descriptor Entries possible). This is a 0’s based<br>value.|||
|12|||Reserved|||

115

**Figure 132: LBA Status Descriptor Entry**

**Bytes**

**Description**

**Status (STAS): This field contains information about this LBA range.**

**Bits**

**Description**
7:3
Reserved

2:0

**LBA Range Status (LBARS): This field indicates information about the logical blocks**
indicated in this LBA Status Descriptor Entry for the Action Type field values supported.

**Value**

**Definition**

**Used with**

**Action Type**

**field Values**

000b
Each logical block may:
•
report Unrecovered Read Error status as
a result of media errors;
•
be a logical block for which the most
recent write to the logical block was a
Write Uncorrectable command; or
•
be read successfully.
10h and 11h

001b
Each logical block may:
•
report Unrecovered Read Error status
as a result of media errors; or
•
be a logical block for which the most
recent write to the logical block was a
Write Uncorrectable command.
10h and 11h

010b
One or more of the reported logical blocks are
allocated.
02h

011b
Each logical block is a:
•
logical block for which the most recent
write to the logical block was a Write
Uncorrectable command.
10h and 11h

100b to 111b
Reserved
15:14
Reserved

The Descriptor Starting LBA (DSLBA) field in the first LBA Status Descriptor Entry returned in the LBA
Status Descriptor List shall contain the lowest numbered LBA that is greater than or equal to the value
specified in the Starting LBA field in the Get LBA Status command.
For subsequent LBA Status Descriptor Entries, the contents of the Descriptor Starting LBA field shall
contain the value of the lowest numbered LBA meeting the requirements for the specified Action Type value
that is greater than or equal to the sum of the values in:
a) the Descriptor Starting LBA field in the previous LBA Status Descriptor Entry; and
b) the Number of Logical Blocks field in the previous LBA Status Descriptor Entry.

**4.2.1.3**

**Command Completion**
When the command is completed, the controller posts a completion queue entry to the Admin Completion
Queue indicating the status for the command.


||Bytes|||Description||
|---|---|---|---|---|---|
|13|||Status (STAS): This field contains information about this LBA range.<br>Bits Description<br>7:3 Reserved<br>LBA Range Status (LBARS): This field indicates information about the logical blocks<br>indicated in this LBA Status Descriptor Entry for the Action Type field values supported.<br>Used with<br>Value Definition Action Type<br>field Values<br>Each logical block may:<br>• report Unrecovered Read Error status as<br>a result of media errors;<br>000b • be a logical block for which the most 10h and 11h<br>recent write to the logical block was a<br>Write Uncorrectable command; or<br>• be read successfully.<br>2:0 Each logical block may:<br>• report Unrecovered Read Error status<br>001b as a result of media errors; or 10h and 11h<br>• be a logical block for which the most<br>recent write to the logical block was a<br>Write Uncorrectable command.<br>One or more of the reported logical blocks are<br>010b 02h<br>allocated.<br>Each logical block is a:<br>• logical block for which the most recent<br>011b 10h and 11h<br>write to the logical block was a Write<br>Uncorrectable command.<br>100b to 111b Reserved|||
|15:14|||Reserved|||


||Bits|||Description||
|---|---|---|---|---|---|
|7:3|||Reserved|||
|2:0|||LBA Range Status (LBARS): This field indicates information about the logical blocks<br>indicated in this LBA Status Descriptor Entry for the Action Type field values supported.<br>Used with<br>Value Definition Action Type<br>field Values<br>Each logical block may:<br>• report Unrecovered Read Error status as<br>a result of media errors;<br>000b • be a logical block for which the most 10h and 11h<br>recent write to the logical block was a<br>Write Uncorrectable command; or<br>• be read successfully.<br>Each logical block may:<br>• report Unrecovered Read Error status<br>001b as a result of media errors; or 10h and 11h<br>• be a logical block for which the most<br>recent write to the logical block was a<br>Write Uncorrectable command.<br>One or more of the reported logical blocks are<br>010b 02h<br>allocated.<br>Each logical block is a:<br>• logical block for which the most recent<br>011b 10h and 11h<br>write to the logical block was a Write<br>Uncorrectable command.<br>100b to 111b Reserved|||


|Value|Definition||Used with||
|---|---|---|---|---|
||||Action Type||
||||field Values||
|000b|Each logical block may:<br>• report Unrecovered Read Error status as<br>a result of media errors;<br>• be a logical block for which the most<br>recent write to the logical block was a<br>Write Uncorrectable command; or<br>• be read successfully.|10h and 11h|||
|001b|Each logical block may:<br>• report Unrecovered Read Error status<br>as a result of media errors; or<br>• be a logical block for which the most<br>recent write to the logical block was a<br>Write Uncorrectable command.|10h and 11h|||
|010b|One or more of the reported logical blocks are<br>allocated.|02h|||
|011b|Each logical block is a:<br>• logical block for which the most recent<br>write to the logical block was a Write<br>Uncorrectable command.|10h and 11h|||
|100b to 111b|Reserved||||

