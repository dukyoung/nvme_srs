NVM Express NVM Command Set Specification, Revision 1.2


24


**3 I/O Commands for the NVM Command Set**

This section specifies the NVM Command Set I/O commands.

**3.1**

**Submission Queue Entry and Completion Queue Entry**

The submission queue entry (SQE) structure and the fields that are common to all NVMe I/O Command
Sets are defined in the Submission Queue Entry section in the NVM Express Base Specification. The
completion queue entry (CQE) structure and the fields that are common to all NVMe I/O Command Sets
are defined in the Completion Queue Entry section in the NVM Express Base Specification. The command
specific fields in the SQE and CQE data structures (i.e., SQE Command Dword 2, Dword 3, Dwords 10-15
and CQE Dword 0, and Dword 1) for the NVM Command Set are defined in the following sections.
Completion queue entries indicate a Status Code Type (SCT) for the type of completion being reported.
The status code type values and descriptions are described in the Status Field Definition section of the

**Common Command Format**
The Common Command Format is as defined in the NVM Express Base Specification.

**NVM Command Set Specific Status Values**

**Figure 17: Status Code – Generic Command Status Values**

**Value**

**Definition**
14h

**Atomic Write Unit Exceeded: The length specified exceeds the atomic write unit size.**

1Eh

**SGL Data Block Granularity Invalid: The Address alignment or Length granularity for an SGL Data**
Block descriptor is invalid. This may occur when a controller supports dword granularity only and the
least significant two bits of the Address or Length are not cleared to 00b.
Note: An implementation compliant with revision 1.2.1 of the NVM Express Base Specification or earlier
may use the status code value of 15h to indicate SGL Data Block Granularity Invalid.
25h

**Invalid Key Tag: The command was denied due to an invalid KEYTAG (refer to section 5.4). Refer to**
the appropriate security specification (e.g., TCG Storage Interface Interactions specification).
80h

**LBA Out of Range: The command references an LBA that exceeds the size of the namespace.**

81h

**Capacity Exceeded: The command requested an operation that exceeds the capacity of the**
namespace. This error occurs when the Namespace Utilization exceeds the Namespace Capacity, as
reported in Figure 114.

**Figure 18: Status Code – Command Specific Status Values**

**Value**

**Definition**

**Commands Affected**
80h
Conflicting Attributes
Dataset Management, Read, Write
81h
Invalid Protection Information
Compare, Copy, Read, Verify, Write, Write Zeroes
82h
Attempted Write to Read Only Range
Copy, Dataset Management, Flush, Format NVM, Write,
Write Uncorrectable, Write Zeroes
83h
Command Size Limit Exceeded
Copy, Dataset Management
85h
Incompatible Namespace or Format
Copy
86h
Fast Copy Not Possible
Copy
87h
Overlapping I/O Range
Copy
89h
Insufficient Resrouces
Copy
8Ah to BFh
Reserved


||Value|||Definition||
|---|---|---|---|---|---|
|14h|||Atomic Write Unit Exceeded: The length specified exceeds the atomic write unit size.|||
|1Eh|||SGL Data Block Granularity Invalid: The Address alignment or Length granularity for an SGL Data<br>Block descriptor is invalid. This may occur when a controller supports dword granularity only and the<br>least significant two bits of the Address or Length are not cleared to 00b.<br>Note: An implementation compliant with revision 1.2.1 of the NVM Express Base Specification or earlier<br>may use the status code value of 15h to indicate SGL Data Block Granularity Invalid.|||
|25h|||Invalid Key Tag: The command was denied due to an invalid KEYTAG (refer to section 5.4). Refer to<br>the appropriate security specification (e.g., TCG Storage Interface Interactions specification).|||
|80h|||LBA Out of Range: The command references an LBA that exceeds the size of the namespace.|||
|81h|||Capacity Exceeded: The command requested an operation that exceeds the capacity of the<br>namespace. This error occurs when the Namespace Utilization exceeds the Namespace Capacity, as<br>reported in Figure 114.|||


||Value|||Definition||Commands Affected|
|---|---|---|---|---|---|---|
|80h|||Conflicting Attributes|||Dataset Management, Read, Write|
|81h|||Invalid Protection Information|||Compare, Copy, Read, Verify, Write, Write Zeroes|
|82h|||Attempted Write to Read Only Range|||Copy, Dataset Management, Flush, Format NVM, Write,<br>Write Uncorrectable, Write Zeroes|
|83h|||Command Size Limit Exceeded|||Copy, Dataset Management|
|85h|||Incompatible Namespace or Format|||Copy|
|86h|||Fast Copy Not Possible|||Copy|
|87h|||Overlapping I/O Range|||Copy|
|89h|||Insufficient Resrouces|||Copy|
|8Ah to BFh|||Reserved||||

25

**Figure 19: Status Code – Media and Data Integrity Error Values**

**Value**

**Definition**
85h

**Compare Failure: The command failed due to a miscompare during a Compare command.**
87h

**Deallocated or Unwritten Logical Block: The command failed due to an attempt to copy from, read**
from, or verify an LBA range containing a deallocated or unwritten logical block.

**3.2**

**I/O Command behavior for the NVM Command Set**

This section defines specific behavior for I/O commands defined in the NVM Express Base Specification
for the NVM Command Set.

**I/O Management Receive command**

**3.2.1.1**

**Reclaim Unit Handle Status (Management Operation 01h)**
The Reclaim Unit Handle Status Descriptor utilized for this management operation for the NVM Command
Set is defined in Figure 20. The Reclaim Unit Handle Status Descriptor in the Reclaim Unit Handle Status
Descriptor List shall be listed first in ascending order of Placement Handle and second in ascending order
of Reclaim Group Identifier.

**Figure 20: Reclaim Unit Handle Status Descriptor**

**Bytes**

**Description**

1:0
Placement Identifier (PID): This field indicates the Placement Identifier (refer to the Reclaim Unit Handle
Status section in the NVM Express Base Specification) containing the Placement Handle and Reclaim
Group Identifier for this Reclaim Unit Handle Status Descriptor.
3:2
Reclaim Unit Handle Identifier (RUHID): This field indicates the Reclaim Unit Handle for the Placement
Identifier field.

7:4

**Estimated Active Reclaim Unit Time Remaining (EARUTR): This field indicates an estimate of the time**
in seconds that the Reclaim Unit currently referenced by the Reclaim Unit Handle is allowed to remain
referenced by that Reclaim Unit Handle (refer to the Flexible Data Placement section in the NVM Express
Base Specification) before the controller may modify the Reclaim Unit Handle to reference a different
Reclaim Unit. This value is the remaining time at the time the I/O Management Receive command is
processed by the controller.
If this field is cleared to 0h, then no time is reported.

15:08
Reclaim Unit Available Media Writes (RUAMW): This field indicates the number of logical blocks which
are currently able to be written to the media associated with the Reclaim Unit currently referenced by the
Placement Identifier field.
The product of this field and the Formatted LBA Size field is able to be less than the nominal size (refer to
the RUNS field in the FDP Configurations log page defined in the NVM Express Base Specification) of the
Reclaim Unit (e.g., the Reclaim Unit has not been written, but excess defects prevent writing some of the
media).
The product of this field and the Formatted LBA Size field is able to be greater than the nominal size (refer
to the RUNS field in the FDP Configurations log page defined in the NVM Express Base Specification) of
the Reclaim Unit (e.g., there is over-provisioned capacity to support the Reclaim Unit).
The value of this field may or may not be modified by a Controller Level Reset or the processing of a Flush
command.
31:16
Reserved

**3.3**

**NVM Command Set Commands**

The NVM Command Set includes the commands listed in Figure 21. This section describes the definition
for each of the commands defined by this specification. Commands are submitted as described in the NVM
Express Base Specification. Physical region page (PRP) entries (refer to the Data Layout section of the


||Value|||Definition||
|---|---|---|---|---|---|
|85h|||Compare Failure: The command failed due to a miscompare during a Compare command.|||
|87h|||Deallocated or Unwritten Logical Block: The command failed due to an attempt to copy from, read<br>from, or verify an LBA range containing a deallocated or unwritten logical block.|||


||Bytes|||Description||
|---|---|---|---|---|---|
|1:0|||Placement Identifier (PID): This field indicates the Placement Identifier (refer to the Reclaim Unit Handle<br>Status section in the NVM Express Base Specification) containing the Placement Handle and Reclaim<br>Group Identifier for this Reclaim Unit Handle Status Descriptor.|||
|3:2|||Reclaim Unit Handle Identifier (RUHID): This field indicates the Reclaim Unit Handle for the Placement<br>Identifier field.|||
|7:4|||Estimated Active Reclaim Unit Time Remaining (EARUTR): This field indicates an estimate of the time<br>in seconds that the Reclaim Unit currently referenced by the Reclaim Unit Handle is allowed to remain<br>referenced by that Reclaim Unit Handle (refer to the Flexible Data Placement section in the NVM Express<br>Base Specification) before the controller may modify the Reclaim Unit Handle to reference a different<br>Reclaim Unit. This value is the remaining time at the time the I/O Management Receive command is<br>processed by the controller.<br>If this field is cleared to 0h, then no time is reported.|||
|15:08|||Reclaim Unit Available Media Writes (RUAMW): This field indicates the number of logical blocks which<br>are currently able to be written to the media associated with the Reclaim Unit currently referenced by the<br>Placement Identifier field.<br>The product of this field and the Formatted LBA Size field is able to be less than the nominal size (refer to<br>the RUNS field in the FDP Configurations log page defined in the NVM Express Base Specification) of the<br>Reclaim Unit (e.g., the Reclaim Unit has not been written, but excess defects prevent writing some of the<br>media).<br>The product of this field and the Formatted LBA Size field is able to be greater than the nominal size (refer<br>to the RUNS field in the FDP Configurations log page defined in the NVM Express Base Specification) of<br>the Reclaim Unit (e.g., there is over-provisioned capacity to support the Reclaim Unit).<br>The value of this field may or may not be modified by a Controller Level Reset or the processing of a Flush<br>command.|||
|31:16|||Reserved|||

26
In the case of Compare, Read, Verify, Write, and Write Zeroes commands, the host may indicate whether
a time limit should be applied to error recovery for the operation by setting the Limited Retry (LR) bit in the
command. The time limit is specified in the Error Recovery feature, specified in section 4.1.3.5. If the host
does not specify a time limit should be applied, then the controller should apply all error recovery means to
complete the operation.
If a host does not set the LBA Format Extension Enable (LBAFEE) field to 1h in the Host Behavior Support
feature (refer to section 4.1.3.6), then a controller aborts all I/O commands that access user data to
namespaces formatted with (refer to section 5.3.1):
a) 16b Guard Protection Information with the STS field set to a non-zero value;
b) 32b Guard Protection Information; and
c) 64b Guard Protection Information.

**Figure 21: Opcodes for NVM Commands**

**Opcode by Field**

**Combined Opcode**

**Command 2**

**Reference Section**

**(07:02)**

**(01:00)**

**Function**

**Data Transfer 3**

0000 00b
00b
00h
Flush 4
NVM Express Base
Specification
0000 00b
01b
01h
Write
3.3.6
0000 00b
10b
02h
Read
3.3.4
0000 01b
00b
04h
Write Uncorrectable
3.3.7
0000 01b
01b
05h
Compare
3.3.1
0000 10b
00b
08h
Write Zeroes
3.3.8
0000 10b
01b
09h
Dataset Management
3.3.3
0000 11b
00b
0Ch
Verify
3.3.5
0000 11b
01b
0Dh
Reservation Register

NVM Express Base
Specification
0000 11b
10b
0Eh
Reservation Report
0001 00b
01b
11h
Reservation Acquire
0001 00b
10b
12h
I/O Management Receive
0001 01b
01b
15h
Reservation Release
0001 10b
00b
18h
Cancel 4
0001 10b
01b
19h
Copy
3.3.2
0001 11b
01b
1Dh
I/O Management Send
NVM Express Base
Specification

**Vendor Specific**
n/a
NOTE 3
80h to FFh
Vendor specific
Notes:
1.
Opcodes not listed are reserved.
2.
All NVM commands use the Namespace Identifier (NSID) field. The value FFFFFFFFh is not supported in this
field unless footnote 4 in this figure indicates that a specific command does support that value.
3.
Indicates the data transfer direction of the command. All options to the command shall transfer data as specified
or transfer no data. All commands, including vendor specific commands, shall follow this convention: 00b = no
data transfer; 01b = host to controller; 10b = controller to host; 11b = bidirectional.
4.
This command may support the use of the Namespace Identifier (NSID) field set to FFFFFFFFh.

**Compare command**
The Compare command reads the logical blocks specified by the command from the non-volatile medium
and compares the data read to a comparison data buffer transferred as part of the command. If the data


||Opcode by Field|||||Combined Opcode<br>1|2<br>Command|Reference Section||
|---|---|---|---|---|---|---|---|---|---|
||(07:02)|||(01:00)||||||
||Function|||3<br>Data Transfer||||||
|0000 00b|||00b|||00h|4<br>Flush|NVM Express Base<br>Specification||
|0000 00b|||01b|||01h|Write|3.3.6||
|0000 00b|||10b|||02h|Read|3.3.4||
|0000 01b|||00b|||04h|Write Uncorrectable|3.3.7||
|0000 01b|||01b|||05h|Compare|3.3.1||
|0000 10b|||00b|||08h|Write Zeroes|3.3.8||
|0000 10b|||01b|||09h|Dataset Management|3.3.3||
|0000 11b|||00b|||0Ch|Verify|3.3.5||
|0000 11b|||01b|||0Dh|Reservation Register|NVM Express Base<br>Specification||
|0000 11b|||10b|||0Eh|Reservation Report|||
|0001 00b|||01b|||11h|Reservation Acquire|||
|0001 00b|||10b|||12h|I/O Management Receive|||
|0001 01b|||01b|||15h|Reservation Release|||
|0001 10b|||00b|||18h|4<br>Cancel|||
|0001 10b|||01b|||19h|Copy|3.3.2||
|0001 11b|||01b|||1Dh|I/O Management Send|NVM Express Base<br>Specification||
||Vendor Specific|||||||||
|n/a|||NOTE 3|||80h to FFh|Vendor specific|||
|Notes:<br>1. Opcodes not listed are reserved.<br>2. All NVM commands use the Namespace Identifier (NSID) field. The value FFFFFFFFh is not supported in this<br>field unless footnote 4 in this figure indicates that a specific command does support that value.<br>3. Indicates the data transfer direction of the command. All options to the command shall transfer data as specified<br>or transfer no data. All commands, including vendor specific commands, shall follow this convention: 00b = no<br>data transfer; 01b = host to controller; 10b = controller to host; 11b = bidirectional.<br>4. This command may support the use of the Namespace Identifier (NSID) field set to FFFFFFFFh.||||||||||

27
read from the controller and the comparison data buffer are equivalent with no miscompares, then the
command completes successfully. If there is any miscompare, the command completes with an error of
Compare Failure.
If metadata is provided, then a comparison is also performed for the metadata, excluding protection
information. The command may specify protection information to be checked as described in section
5.3.2.4.
The command uses Command Dword 2, Command Dword 3, Command Dword 10, Command Dword 11,
Command Dword 12, Command Dword 13, Command Dword 14, and Command Dword 15 fields. If the
command uses PRPs for the data transfer, then the Metadata Pointer, PRP Entry 1, and PRP Entry 2 fields
are used. If the command uses SGLs for the data transfer, then the Metadata SGL Segment Pointer and
SGL Entry 1 fields are used. All other command specific fields are reserved.

**Figure 22: Compare – Metadata Pointer**

**Bits**

**Description**
63:00
Metadata Pointer (MPTR): This field contains the Metadata Pointer, if applicable. Refer to the Common
Command Format figure in the NVM Express Base Specification for the definition of this field.

**Figure 23: Compare – Data Pointer**

**Bits**

**Description**
127:00

**Data Pointer (DPTR): This field specifies the data to use for the compare. Refer to the Common**
Command Format figure in the NVM Express Base Specification for the definition of this field.

**Figure 24: Compare – Command Dword 2 and Dword 3**

**Bits**

**Description**
63:48
Reserved

47:00

**Expected Logical Block Tags Upper (ELBTU): This field and Command Dword 14 specify the variable**
sized Expected Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag
(EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-
end protection information, then this field is ignored by the controller.

**Figure 25: Compare – Command Dword 10 and Command Dword 11**

**Bits**

**Description**

63:00
Starting LBA (SLBA): This field specifies the 64-bit address of the first logical block to compare against
as part of the operation. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits
63:32.

**Figure 26: Compare – Command Dword 12**

**Bits**

**Description**
Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this bit
is cleared to ‘0’, then the controller should apply all available error recovery means to retrieve the data
for comparison.
Force Unit Access (FUA): If this bit is set to ‘1’, then for data and metadata, if any, associated with
logical blocks specified by the Compare command, the controller shall:
1)
commit that data and metadata, if any, to non-volatile medium; and
2)
read the data and metadata, if any, from non-volatile medium.
If this bit is cleared to ‘0’, then this bit has no effect.


||Bits|||Description||
|---|---|---|---|---|---|
|63:00|||Metadata Pointer (MPTR): This field contains the Metadata Pointer, if applicable. Refer to the Common<br>Command Format figure in the NVM Express Base Specification for the definition of this field.|||


||Bits|||Description||
|---|---|---|---|---|---|
|127:00|||Data Pointer (DPTR): This field specifies the data to use for the compare. Refer to the Common<br>Command Format figure in the NVM Express Base Specification for the definition of this field.|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:48|||Reserved|||
|47:00|||Expected Logical Block Tags Upper (ELBTU): This field and Command Dword 14 specify the variable<br>sized Expected Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag<br>(EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-<br>end protection information, then this field is ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:00|||Starting LBA (SLBA): This field specifies the 64-bit address of the first logical block to compare against<br>as part of the operation. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits<br>63:32.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31|||Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this bit<br>is cleared to ‘0’, then the controller should apply all available error recovery means to retrieve the data<br>for comparison.|||
|30|||Force Unit Access (FUA): If this bit is set to ‘1’, then for data and metadata, if any, associated with<br>logical blocks specified by the Compare command, the controller shall:<br>1) commit that data and metadata, if any, to non-volatile medium; and<br>2) read the data and metadata, if any, from non-volatile medium.<br>If this bit is cleared to ‘0’, then this bit has no effect.|||

28

**Figure 26: Compare – Command Dword 12**

**Bits**

**Description**

29:26

**Protection Information (PRINFO): Specifies the protection information action and check field, as**
defined in Figure 11. The Protection Information Action (PRACT) bit shall be cleared to ‘0’. If the
Protection Information Check (PRCHK) field is non-zero, protection checks are performed on the logical
blocks transferred from the host and on the logical blocks read from NVM (refer to section 5.3.2.4).
Reserved
Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of end-to-
end data protection processing as defined in Figure 12.
23:20
Reserved
19:16

**Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the**
command (refer to the Key Per I/O section in the NVM Express Base Specification).

**15:00**

**Number of Logical Blocks (NLB): This field specifies the number of logical blocks to be compared.**

**This is a 0’s based value.**

The definition of Command Dword 13 is based on the CETYPE value. If the CETYPE value is cleared to
0h, then Command Dword 13 is reserved. If the CETYPE value is non-zero, then Command Dword 13 is
defined in Figure 27.

**Figure 27: Compare - Command Dword 13 if CETYPE is non-zero**

**Bits**

**Description**
31:16
Reserved
15:00

**Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE**
field. Refer to the Key Per I/O section in the NVM Express Base Specification.

**Figure 28: Compare – Command Dword 14**

**Bits**

**Description**

31:00

**Expected Logical Block Tags Lower (ELBTL): This field and bits 47:00 of Command Dword 2 and**
Dword 3 specify the variable sized Expected Logical Block Storage Tag (ELBST) and Expected Initial
Logical Block Reference Tag (EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace
is not formatted to use end-to-end protection information, then this field is ignored by the controller.

**Figure 29: Compare – Command Dword 15**

**Bits**

**Description**

31:16

**Expected Logical Block Application Tag Mask (ELBATM): This field specifies the Application Tag**
Mask expected value. If the namespace is not formatted to use end-to-end protection information, then
this field is ignored by the controller. Refer to section 5.3.

15:00

**Expected Logical Block Application Tag (ELBAT): This field specifies the Application Tag expected**
value. If the namespace is not formatted to use end-to-end protection information, then this field is
ignored by the controller. Refer to section 5.3.

**3.3.1.1**

**Command Completion**
If the command is completed, then the controller shall post a completion queue entry to the associated I/O
Completion Queue indicating the status for the command. If there are any miscompares between the data
read from the NVM media and the data buffer provided, then the command fails with a status code of
Compare Failure.
Compare command specific status values are defined in Figure 30.


||Bits|||Description||
|---|---|---|---|---|---|
|29:26|||Protection Information (PRINFO): Specifies the protection information action and check field, as<br>defined in Figure 11. The Protection Information Action (PRACT) bit shall be cleared to ‘0’. If the<br>Protection Information Check (PRCHK) field is non-zero, protection checks are performed on the logical<br>blocks transferred from the host and on the logical blocks read from NVM (refer to section 5.3.2.4).|||
|25|||Reserved|||
|24|||Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of end-to-<br>end data protection processing as defined in Figure 12.|||
|23:20|||Reserved|||
|19:16|||Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the<br>command (refer to the Key Per I/O section in the NVM Express Base Specification).|||
|15:00|||Number of Logical Blocks (NLB): This field specifies the number of logical blocks to be compared.<br>This is a 0’s based value.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Reserved|||
|15:00|||Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE<br>field. Refer to the Key Per I/O section in the NVM Express Base Specification.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:00|||Expected Logical Block Tags Lower (ELBTL): This field and bits 47:00 of Command Dword 2 and<br>Dword 3 specify the variable sized Expected Logical Block Storage Tag (ELBST) and Expected Initial<br>Logical Block Reference Tag (EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace<br>is not formatted to use end-to-end protection information, then this field is ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Expected Logical Block Application Tag Mask (ELBATM): This field specifies the Application Tag<br>Mask expected value. If the namespace is not formatted to use end-to-end protection information, then<br>this field is ignored by the controller. Refer to section 5.3.|||
|15:00|||Expected Logical Block Application Tag (ELBAT): This field specifies the Application Tag expected<br>value. If the namespace is not formatted to use end-to-end protection information, then this field is<br>ignored by the controller. Refer to section 5.3.|||

29

**Figure 30: Compare – Command Specific Status Values**

**Value**

**Definition**

81h
Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 26) settings
specified in the command are invalid for the Protection Information with which the namespace was
formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the EILBRT field is invalid

**(refer to section 5.3.3).**

**Copy command**
The Copy command is used by the host to copy user data from one or more source ranges in one or more
source namespaces to a single consecutive destination logical block range in a destination namespace
(i.e., the namespace specified by the NSID field). Each source range may be in the same namespace or a
different namespace with respect to any other source range and with respect to the destination logical block
range.
The command uses Command Dword 2, Command Dword 3, Command Dword 10, Command Dword 11,
Command Dword 12, Command Dword 13, Command Dword 14, and Command Dword 15 fields. If the
command uses PRPs for the data transfer, then the PRP Entry 1 and PRP Entry 2 fields are used. If the
command uses SGLs for the data transfer, then the SGL Entry 1 field is used. All other command specific
fields are reserved.

**Figure 31: Copy – Data Pointer**

**Bits**

**Description**
127:00

**Data Pointer (DPTR): This field specifies the data to use for the command. Refer to the Common**
Command Format figure in the NVM Express Base Specification for the definition of this field.

**Figure 32: Copy – Command Dword 2 and Dword 3**

**Bits**

**Description**
63:48
Reserved

47:00

**Logical Block Tags Upper (LBTU): This field and Command Dword 14 specify the variable sized**
Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT) fields, which are
defined in section 5.3.1.4.1, to be used for the write portion of the copy operation. If the destination
namespace is not formatted to use end-to-end protection information, then this field is ignored by the
controller.

**Figure 33: Copy – Command Dword 10 and Command Dword 11**

**Bits**

**Description**

63:00
Starting Destination LBA (SDLBA): This field indicates the 64-bit address of the first logical block to
be written as part of the copy operation. Command Dword 10 contains bits 31:00; Command Dword 11
contains bits 63:32.

**Figure 34: Copy – Command Dword 12**

**Bits**

**Description**
Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts for the write
portion of the copy operation. If this bit is cleared to ‘0’, then the controller should apply all available error
recovery means to write the data to the NVM.


||Value||Definition||
|---|---|---|---|---|
|81h||Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 26) settings<br>specified in the command are invalid for the Protection Information with which the namespace was<br>formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the EILBRT field is invalid<br>(refer to section 5.3.3).|||


||Bits||Description||
|---|---|---|---|---|
|127:00|||Data Pointer (DPTR): This field specifies the data to use for the command. Refer to the Common<br>Command Format figure in the NVM Express Base Specification for the definition of this field.||


||Bits||Description||
|---|---|---|---|---|
|63:48|||Reserved||
|47:00|||Logical Block Tags Upper (LBTU): This field and Command Dword 14 specify the variable sized<br>Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT) fields, which are<br>defined in section 5.3.1.4.1, to be used for the write portion of the copy operation. If the destination<br>namespace is not formatted to use end-to-end protection information, then this field is ignored by the<br>controller.||


||Bits||Description||
|---|---|---|---|---|
|63:00|||Starting Destination LBA (SDLBA): This field indicates the 64-bit address of the first logical block to<br>be written as part of the copy operation. Command Dword 10 contains bits 31:00; Command Dword 11<br>contains bits 63:32.||


||Bits||Description||
|---|---|---|---|---|
|31|||Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts for the write<br>portion of the copy operation. If this bit is cleared to ‘0’, then the controller should apply all available error<br>recovery means to write the data to the NVM.||

30

**Figure 34: Copy – Command Dword 12**

**Bits**

**Description**
Force Unit Access (FUA): If this bit is set to ‘1’, then for data and metadata, if any, associated with
logical blocks specified by the write portion of the copy operation, the controller shall write that data and
metadata, if any, to non-volatile medium before indicating command completion.
There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has no effect.
29:26
Protection Information Write (PRINFOW): Specifies the protection information action and check field,
as defined in Figure 11, to be used for the write portion of the copy operation.

**Storage Tag Check Read (STCR): This bit specifies the Storage Tag field shall be checked as part of**
end-to-end data protection processing as defined in Figure 12, to be used for the read portion of the copy
operation. If the Storage Tag Check Read Support (STCRS) bit (refer to Figure 111) is cleared to ‘0’,
then this bit is reserved.
Storage Tag Check Write (STCW): This bit specifies the Storage Tag field shall be checked as part of
end-to-end data protection processing as defined in Figure 12, to be used for the write portion of the
copy operation.

**23:20**
Directive Type (DTYPE): Specifies the Directive Type associated with the Directive Specific field (refer
to the Directives section in the NVM Express Base Specification) used for the write portion of the copy
operation.

19:16

**Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the**
command (refer to the Key Per I/O section in the NVM Express Base Specification). This field is used for
the write portion of the copy operation.

15:12

**Protection Information Read (PRINFOR): Specifies the protection information action and check field,**
as defined in Figure 11, to be used for the read portion of the copy operation specified by each Source

**Range entries.**

11:08

**Descriptor Format (DESFMT): Specifies the type of the Copy Descriptor Format that is used. The Copy**
Descriptor Format specifies the starting location, length, and parameters associated with the read portion
of the operation.

**Code Descriptor**

**Format Type**

**Definition**
0h
Source Range Entries Copy Descriptor Format 0h is used (refer to Figure 39).
1h
Source Range Entries Copy Descriptor Format 1h is used (refer to Figure 40).
2h
Source Range Entries Copy Descriptor Format 2h is used (refer to Figure 39).
3h
Source Range Entries Copy Descriptor Format 3h is used (refer to Figure 40).

4h
Source Range Entries Copy Descriptor Format 4h is used (refer to the
Memory Copy command section of the NVM Express Subsystem Local
Memory Command Set Specification).
All Others
Reserved
07:00

**Number of Ranges (NR): Specifies the number of Source Range entries that are specified in the**
command. This is a 0’s-based value.

**Figure 35: Copy – Command Dword 13**

**Bits**

**Description**
31:16
Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type
field (refer to the Directives section in the NVM Express Base Specification).

15:00

**Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE**
field. Refer to the Key Per I/O section in the NVM Express Base Specification. This field is used for the
write portion of the copy operation.


||Bits|||Description||
|---|---|---|---|---|---|
|30|||Force Unit Access (FUA): If this bit is set to ‘1’, then for data and metadata, if any, associated with<br>logical blocks specified by the write portion of the copy operation, the controller shall write that data and<br>metadata, if any, to non-volatile medium before indicating command completion.<br>There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has no effect.|||
|29:26|||Protection Information Write (PRINFOW): Specifies the protection information action and check field,<br>as defined in Figure 11, to be used for the write portion of the copy operation.|||
|25|||Storage Tag Check Read (STCR): This bit specifies the Storage Tag field shall be checked as part of<br>end-to-end data protection processing as defined in Figure 12, to be used for the read portion of the copy<br>operation. If the Storage Tag Check Read Support (STCRS) bit (refer to Figure 111) is cleared to ‘0’,<br>then this bit is reserved.|||
|24|||Storage Tag Check Write (STCW): This bit specifies the Storage Tag field shall be checked as part of<br>end-to-end data protection processing as defined in Figure 12, to be used for the write portion of the<br>copy operation.|||
|23:20|||Directive Type (DTYPE): Specifies the Directive Type associated with the Directive Specific field (refer<br>to the Directives section in the NVM Express Base Specification) used for the write portion of the copy<br>operation.|||
|19:16|||Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the<br>command (refer to the Key Per I/O section in the NVM Express Base Specification). This field is used for<br>the write portion of the copy operation.|||
|15:12|||Protection Information Read (PRINFOR): Specifies the protection information action and check field,<br>as defined in Figure 11, to be used for the read portion of the copy operation specified by each Source<br>Range entries.|||
|11:08|||Descriptor Format (DESFMT): Specifies the type of the Copy Descriptor Format that is used. The Copy<br>Descriptor Format specifies the starting location, length, and parameters associated with the read portion<br>of the operation.<br>Code Descriptor<br>Definition<br>Format Type<br>0h Source Range Entries Copy Descriptor Format 0h is used (refer to Figure 39).<br>1h Source Range Entries Copy Descriptor Format 1h is used (refer to Figure 40).<br>2h Source Range Entries Copy Descriptor Format 2h is used (refer to Figure 39).<br>3h Source Range Entries Copy Descriptor Format 3h is used (refer to Figure 40).<br>Source Range Entries Copy Descriptor Format 4h is used (refer to the<br>4h Memory Copy command section of the NVM Express Subsystem Local<br>Memory Command Set Specification).<br>All Others Reserved|||
|07:00|||Number of Ranges (NR): Specifies the number of Source Range entries that are specified in the<br>command. This is a 0’s-based value.|||


||Code Descriptor||Definition|
|---|---|---|---|
||Format Type|||
|0h|||Source Range Entries Copy Descriptor Format 0h is used (refer to Figure 39).|
|1h|||Source Range Entries Copy Descriptor Format 1h is used (refer to Figure 40).|
|2h|||Source Range Entries Copy Descriptor Format 2h is used (refer to Figure 39).|
|3h|||Source Range Entries Copy Descriptor Format 3h is used (refer to Figure 40).|
|4h|||Source Range Entries Copy Descriptor Format 4h is used (refer to the<br>Memory Copy command section of the NVM Express Subsystem Local<br>Memory Command Set Specification).|
|All Others|||Reserved|


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type<br>field (refer to the Directives section in the NVM Express Base Specification).|||
|15:00|||Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE<br>field. Refer to the Key Per I/O section in the NVM Express Base Specification. This field is used for the<br>write portion of the copy operation.|||

31

**Figure 36: Copy – Command Dword 14**

**Bits**

**Description**

31:00

**Logical Block Tags Lower (LBTL): This field and bits 47:00 of Command Dword 2 and Dword 3 specify**
the variable sized Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT)
fields, which are defined in section 5.3.1.4.1, to be used for the write portion of the copy operation. If the
destination namespace is not formatted to use end-to-end protection information, then this field is ignored
by the controller.

**Figure 37: Copy – Command Dword 15**

**Bits**

**Description**

31:16

**Logical Block Application Tag Mask (LBATM): This field specifies the Application Tag Mask value for**
the write portion of the copy operation. If the destination namespace is not formatted to use end-to-end
protection information, then this field is ignored by the controller. Refer to section 5.3.

15:00

**Logical Block Application Tag (LBAT): This field specifies the Application Tag value for the write**
portion of the copy operation. If the destination namespace is not formatted to use end-to-end protection
information, then this field is ignored by the controller. Refer to section 5.3.

The controller shall indicate the Source Range Entries Copy Descriptor Formats supported by the controller
in the Copy Descriptor Formats Supported field in the Identify Controller data structure (refer to the NVM
Express Base Specification).
Controller usage of Source Range Entries Copy Descriptor Formats 2h and 3h is further qualified by
whether the host has enabled these formats in the Host Behavior Support feature (refer to the NVM Express
Base Specification). If the controller supports a Source Range Entries Copy Descriptor Format that has not
been enabled, the controller shall process Copy commands as if that format is not supported (e.g., if that
format is specified in the Descriptor Format field in Command Dword 12, the controller shall abort the
command with a status code of Invalid Field in Command). Source Range Entries Copy Descriptor Formats
0h and 1h are always enabled if supported. A host that enables Source Range Entries Copy Descriptor
Formats 2h and/or 3h indicates to the controller that the host accepts the implications (e.g., for namespace
access control) of the presence of a Source Namespace Identifier (SNSID) in these formats (refer to Figure
39 and Figure 40).
The data that the Copy command provides is a list of Source Range entries that describe the data to be
copied to the destination range starting at the LBA specified by the SDLBA field. The Copy Descriptor
Format type of the Source Range entries is specified in the Descriptor Format field in Command Dword 12.
The Copy Descriptor Format types are distinguished by the supported protection information formats (refer
to section 5.3.1) and whether the Copy Descriptor Format contains a Source Namespace Identifier (SNSID)
field that supports a copy source in a different namespace than the copy destination, as described in Figure
38. For a Copy Descriptor Format that does not contain an SNSID field, the source namespace is the same
as the destination namespace which is specified by the NSID field in the command.

**Figure 38: Copy – Copy Descriptor Formats**

**Copy Descriptor**

**Format type**

**Protection Information Formats**

**SNSID field**

**present**

**Description**

0h
16b Guard Protection Information
No
Protection Information size: 8 bytes,
source namespace and destination
namespace are the same.


||Bits|||Description||
|---|---|---|---|---|---|
|31:00|||Logical Block Tags Lower (LBTL): This field and bits 47:00 of Command Dword 2 and Dword 3 specify<br>the variable sized Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT)<br>fields, which are defined in section 5.3.1.4.1, to be used for the write portion of the copy operation. If the<br>destination namespace is not formatted to use end-to-end protection information, then this field is ignored<br>by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Logical Block Application Tag Mask (LBATM): This field specifies the Application Tag Mask value for<br>the write portion of the copy operation. If the destination namespace is not formatted to use end-to-end<br>protection information, then this field is ignored by the controller. Refer to section 5.3.|||
|15:00|||Logical Block Application Tag (LBAT): This field specifies the Application Tag value for the write<br>portion of the copy operation. If the destination namespace is not formatted to use end-to-end protection<br>information, then this field is ignored by the controller. Refer to section 5.3.|||


||Copy Descriptor||Protection Information Formats||SNSID field||Description|
|---|---|---|---|---|---|---|---|
||Format type||||present|||
|0h|||16b Guard Protection Information|No|||Protection Information size: 8 bytes,<br>source namespace and destination<br>namespace are the same.|

32

**Figure 38: Copy – Copy Descriptor Formats**

**Copy Descriptor**

**Format type**

**Protection Information Formats**

**SNSID field**

**present**

**Description**

1h
32b Guard Protection Information
64b Guard Protection Information
No
Protection Information size: 16 bytes,
source namespace and destination
namespace are the same.

2h
16b Guard Protection Information
Yes
Protection Information size: 8 bytes,
source namespace may differ from
destination namespace.

3h
32b Guard Protection Information
64b Guard Protection Information
Yes
Protection Information size: 16 bytes,
source namespace may differ from
destination namespace.

4h
None
Yes
The source namespace supports the
Subsystem
Local
Memory
(SLM)
Command Set (refer to the NVM
Express Subsystem Local Memory
Command Set Specification).

If the Copy Descriptor Format specified in the Descriptor Format field is not supported by the controller,
then the command shall be aborted with a status code of Invalid Field in Command.
If:
a) the Copy Descriptor Format specified in the Descriptor Format field is supported by the controller;
b) the specified destination namespace is formatted to use 16b Guard Protection Information; and
c) the Descriptor Format field is not cleared to 0h and is not set to 2h,
then the command shall be aborted with a status code of Invalid Namespace or Format.
If:
a) the Copy Descriptor Format specified in the Descriptor Format field is supported by the controller;
b) the specified destination namespace is formatted to use 32b Guard Protection Information or 64b
Guard Protection Information; and
c) the Descriptor Format field is not set to 1h and is not set to 3h,
then the command shall be aborted with a status code of Invalid Namespace or Format.
Figure 39 shows the Copy Descriptor Format 0h and Format 2h descriptors with an example that has 128
Source Range entries.

**Figure 39: Copy – Source Range Entries Copy Descriptor Format 0h and Format 2h**

**Range**

**Bytes**

**Description**

Source
Range 0
03:00

**Source Parameters (SPARS): This field specifies attributes as follows:**

**Format 0h**

**bytes**

**Format 2h**

**bytes**

**Description**
03:00
n/a
Reserved
n/a
03:00

**Source Namespace Identifier (SNSID): Specifies the**
source namespace for this Source Range entry.
07:04
Reserved
15:08

**Starting LBA (SLBA)**


||Copy Descriptor||Protection Information Formats||SNSID field||Description|
|---|---|---|---|---|---|---|---|
||Format type||||present|||
|1h|||32b Guard Protection Information<br>64b Guard Protection Information|No|||Protection Information size: 16 bytes,<br>source namespace and destination<br>namespace are the same.|
|2h|||16b Guard Protection Information|Yes|||Protection Information size: 8 bytes,<br>source namespace may differ from<br>destination namespace.|
|3h|||32b Guard Protection Information<br>64b Guard Protection Information|Yes|||Protection Information size: 16 bytes,<br>source namespace may differ from<br>destination namespace.|
|4h|||None|Yes|||The source namespace supports the<br>Subsystem Local Memory (SLM)<br>Command Set (refer to the NVM<br>Express Subsystem Local Memory<br>Command Set Specification).|


||Range|||Bytes|||Description||
|---|---|---|---|---|---|---|---|---|
|Source<br>Range 0|||03:00|||Source Parameters (SPARS): This field specifies attributes as follows:<br>Format 0h Format 2h<br>Description<br>bytes bytes<br>03:00 n/a Reserved<br>Source Namespace Identifier (SNSID): Specifies the<br>n/a 03:00<br>source namespace for this Source Range entry.|||
||||07:04|||Reserved|||
||||15:08|||Starting LBA (SLBA)|||


||Format 0h|||Format 2h||Description|
|---|---|---|---|---|---|---|
||bytes|||bytes|||
|03:00|||n/a|||Reserved|
|n/a|||03:00|||Source Namespace Identifier (SNSID): Specifies the<br>source namespace for this Source Range entry.|

33

**Figure 39: Copy – Source Range Entries Copy Descriptor Format 0h and Format 2h**

**Range**

**Bytes**

**Description**

19:16

**Read Parameters (RPARS): This field specifies attributes as follows.**

**Bits**

**Description**
31:20
Reserved

19:16

**Command Extension Type (CETYPE): Specifies the Command Extension**
Type that applies to the command (refer to the Key Per I/O section in the

the copy operation for the LBAs specified in this Source Range entry.
15:00

**Number of Logical Blocks (NLB): This field indicates the number of logical**
blocks to be copied. This is a 0’s based value.

21:20

**Command Extension Value (CEV): The definition of this field is dependent on the value**
of the CETYPE field. Refer to the Key Per I/O section in the NVM Express Base
Specification. This field is used for the read portion of the copy operation for the LBAs
specified in this Source Range entry.

23:22

**Source Options (SOPT): This field specifies options as follows:**

**Format**

**0h bits**

**Format**

**2h bits**

**Description**

n/a

**Fast Copy Only (FCO): If this bit is set to ‘1’, then the**
controller only performs fast copy operations (refer to section
3.3.2.1) for user data in this Source Range entry. If this bit is
cleared to ‘0’, then this bit has no effect.
15:00
14:00
Reserved

27:24

**Expected Logical Block Tags (ELBT): This field specifies the variable sized Expected**
Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag
(EILBRT), which are defined in section 5.3.1.4.1, to be used for the read portion of the
copy operation for the LBAs specified in this Source Range entry. If the source namespace
is not formatted to use end-to-end protection information, then this field is ignored by the
controller. Refer to section 5.3.

29:28

**Expected Logical Block Application Tag (ELBAT): This field specifies the Application**
Tag expected value used for the read portion of the copy operation for the LBAs specified
in this Source Range entry. If the source namespace is not formatted to use end-to-end

**protection information, then this field is ignored by the controller. Refer to section 5.3.**

31:30

**Expected Logical Block Application Tag Mask (ELBATM): This field specifies the**
Application Tag Mask expected value used for the read portion of the copy operation for
the LBAs specified in this Source Range entry. If the source namespace is not formatted
to use end-to-end protection information, then this field is ignored by the controller. Refer
to section 5.3.

Source
Range 1
35:32

**Source Parameters (SPARS)**
39:36
Reserved
47:40

**Starting LBA (SLBA)**
51:48

**Read Parameters (RPARS)**
53:52

**Command Extension Type (CEV)**
55:54

**Source Options (SOPT)**
59:56

**Expected Logical Block Tags (ELBT): (i.e., ELBST and EILBRT)**
61:60

**Expected Logical Block Application Tag (ELBAT)**
63:62

**Expected Logical Block Application Tag Mask (ELBATM)**
…

Source
Range 127
4067:4064

**Source Parameters (SPARS)**
4071:4068
Reserved
4079:4072

**Starting LBA (SLBA)**
4083:4080

**Read Parameters (RPARS)**
4085:4084

**Command Extension Type (CEV)**
4087:4086

**Source Options (SOPT)**


||Range|||Bytes|||Description||
|---|---|---|---|---|---|---|---|---|
||||19:16|||Read Parameters (RPARS): This field specifies attributes as follows.<br>Bits Description<br>31:20 Reserved<br>Command Extension Type (CETYPE): Specifies the Command Extension<br>Type that applies to the command (refer to the Key Per I/O section in the<br>19:16<br>NVM Express Base Specification). This field is used for the read portion of<br>the copy operation for the LBAs specified in this Source Range entry.<br>Number of Logical Blocks (NLB): This field indicates the number of logical<br>15:00<br>blocks to be copied. This is a 0’s based value.|||
||||21:20|||Command Extension Value (CEV): The definition of this field is dependent on the value<br>of the CETYPE field. Refer to the Key Per I/O section in the NVM Express Base<br>Specification. This field is used for the read portion of the copy operation for the LBAs<br>specified in this Source Range entry.|||
||||23:22|||Source Options (SOPT): This field specifies options as follows:<br>Format Format<br>Description<br>0h bits 2h bits<br>Fast Copy Only (FCO): If this bit is set to ‘1’, then the<br>controller only performs fast copy operations (refer to section<br>n/a 15<br>3.3.2.1) for user data in this Source Range entry. If this bit is<br>cleared to ‘0’, then this bit has no effect.<br>15:00 14:00 Reserved|||
||||27:24|||Expected Logical Block Tags (ELBT): This field specifies the variable sized Expected<br>Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag<br>(EILBRT), which are defined in section 5.3.1.4.1, to be used for the read portion of the<br>copy operation for the LBAs specified in this Source Range entry. If the source namespace<br>is not formatted to use end-to-end protection information, then this field is ignored by the<br>controller. Refer to section 5.3.|||
||||29:28|||Expected Logical Block Application Tag (ELBAT): This field specifies the Application<br>Tag expected value used for the read portion of the copy operation for the LBAs specified<br>in this Source Range entry. If the source namespace is not formatted to use end-to-end<br>protection information, then this field is ignored by the controller. Refer to section 5.3.|||
||||31:30|||Expected Logical Block Application Tag Mask (ELBATM): This field specifies the<br>Application Tag Mask expected value used for the read portion of the copy operation for<br>the LBAs specified in this Source Range entry. If the source namespace is not formatted<br>to use end-to-end protection information, then this field is ignored by the controller. Refer<br>to section 5.3.|||
||||||||||
|Source<br>Range 1|||35:32|||Source Parameters (SPARS)|||
||||39:36|||Reserved|||
||||47:40|||Starting LBA (SLBA)|||
||||51:48|||Read Parameters (RPARS)|||
||||53:52|||Command Extension Type (CEV)|||
||||55:54|||Source Options (SOPT)|||
||||59:56|||Expected Logical Block Tags (ELBT): (i.e., ELBST and EILBRT)|||
||||61:60|||Expected Logical Block Application Tag (ELBAT)|||
||||63:62|||Expected Logical Block Application Tag Mask (ELBATM)|||
||…||||||||
|Source<br>Range 127|||4067:4064|||Source Parameters (SPARS)|||
||||4071:4068|||Reserved|||
||||4079:4072|||Starting LBA (SLBA)|||
||||4083:4080|||Read Parameters (RPARS)|||
||||4085:4084|||Command Extension Type (CEV)|||
||||4087:4086|||Source Options (SOPT)|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:20|||Reserved|||
|19:16|||Command Extension Type (CETYPE): Specifies the Command Extension<br>Type that applies to the command (refer to the Key Per I/O section in the<br>NVM Express Base Specification). This field is used for the read portion of<br>the copy operation for the LBAs specified in this Source Range entry.|||
|15:00|||Number of Logical Blocks (NLB): This field indicates the number of logical<br>blocks to be copied. This is a 0’s based value.|||


||Format|||Format||Description|
|---|---|---|---|---|---|---|
||0h bits|||2h bits|||
|n/a|||15|||Fast Copy Only (FCO): If this bit is set to ‘1’, then the<br>controller only performs fast copy operations (refer to section<br>3.3.2.1) for user data in this Source Range entry. If this bit is<br>cleared to ‘0’, then this bit has no effect.|
|15:00|||14:00|||Reserved|

34

**Figure 39: Copy – Source Range Entries Copy Descriptor Format 0h and Format 2h**

**Range**

**Bytes**

**Description**
4091:4088

**Expected Logical Block Tags (ELBT): (i.e., ELBST and EILBRT)**
4093:4092

**Expected Logical Block Application Tag (ELBAT)**
4095:4094

**Expected Logical Block Application Tag Mask (ELBATM)**

The SNSID field (refer to Figure 39) specifies an active NSID that identifies the namespace for the source
range. If the SNSID field contains an invalid NSID, the value 0h or the value FFFFFFFFh, then the controller
shall abort the Copy command with a status code of Invalid Namespace or Format. If the SNSID field
contains an inactive NSID, then the controller shall abort the Copy command with a status code of Invalid
Field in Command. If the SNSID field contains an active NSID that identifies a namespace that is not
comprised of logical blocks (refer to section 2.1), then the controller:
•
shall abort the Copy command with one of the following three status codes:
o
Invalid Namespace or Format;
o
Incompatible Namespace or Format; or
o
Invalid Field in Command;
and
•
should use the Invalid Namespace or Format status code to abort that Copy command.
Figure 40 shows the Copy Descriptor Format 1h and Format 3h descriptors with an example that has 102
Source Range entries.

**Figure 40: Copy – Source Range Entries Copy Descriptor Format 1h and Format 3h**

**Range**

**Bytes**

**Description**

Source
Range 0
03:00

**Source Parameters (SPARS): This field specifies attributes as follows:**

**Format 1h**

**bytes**

**Format 3h**

**bytes**

**Description**
03:00
n/a
Reserved
n/a
03:00

**Source Namespace Identifier (SNSID): Specifies the**
source namespace for this Source Range entry.
07:04
Reserved
15:08

**Starting LBA (SLBA)**

19:16

**Read Parameters (RPARS): This field specifies attributes as follows:**

**Bits**

**Description**
31:20
Reserved

19:16

**Command Extension Type (CETYPE): Specifies the Command Extension**
Type that applies to the command (refer to the Key Per I/O section in the

**the copy operation for the LBAs specified in this Source Range entry.**
15:00

**Number of Logical Blocks (NLB): This field indicates the number of logical**
blocks to be copied. This is a 0’s based value.

21:20

**Command Extension Value (CEV): The definition of this field is dependent on the value**
of the CETYPE field. Refer to the Key Per I/O section in the NVM Express Base
Specification. This field is used for the read portion of the copy operation for the LBAs
specified in this Source Range entry.


||Range|||Bytes||Description||
|---|---|---|---|---|---|---|---|
||||4091:4088||Expected Logical Block Tags (ELBT): (i.e., ELBST and EILBRT)|||
||||4093:4092||Expected Logical Block Application Tag (ELBAT)|||
||||4095:4094||Expected Logical Block Application Tag Mask (ELBATM)|||


||Range|||Bytes|||Description||
|---|---|---|---|---|---|---|---|---|
|Source<br>Range 0|||03:00|||Source Parameters (SPARS): This field specifies attributes as follows:<br>Format 1h Format 3h<br>Description<br>bytes bytes<br>03:00 n/a Reserved<br>Source Namespace Identifier (SNSID): Specifies the<br>n/a 03:00<br>source namespace for this Source Range entry.|||
||||07:04|||Reserved|||
||||15:08|||Starting LBA (SLBA)|||
||||19:16|||Read Parameters (RPARS): This field specifies attributes as follows:<br>Bits Description<br>31:20 Reserved<br>Command Extension Type (CETYPE): Specifies the Command Extension<br>Type that applies to the command (refer to the Key Per I/O section in the<br>19:16<br>NVM Express Base Specification). This field is used for the read portion of<br>the copy operation for the LBAs specified in this Source Range entry.<br>Number of Logical Blocks (NLB): This field indicates the number of logical<br>15:00<br>blocks to be copied. This is a 0’s based value.|||
||||21:20|||Command Extension Value (CEV): The definition of this field is dependent on the value<br>of the CETYPE field. Refer to the Key Per I/O section in the NVM Express Base<br>Specification. This field is used for the read portion of the copy operation for the LBAs<br>specified in this Source Range entry.|||


|Format 1h<br>bytes|||Format 3h||Description|
|---|---|---|---|---|---|
||||bytes|||
|03:00||n/a|||Reserved|
|n/a||03:00|||Source Namespace Identifier (SNSID): Specifies the<br>source namespace for this Source Range entry.|


|Bits|||Description||
|---|---|---|---|---|
|31:20||Reserved|||
|19:16||Command Extension Type (CETYPE): Specifies the Command Extension<br>Type that applies to the command (refer to the Key Per I/O section in the<br>NVM Express Base Specification). This field is used for the read portion of<br>the copy operation for the LBAs specified in this Source Range entry.|||
|15:00||Number of Logical Blocks (NLB): This field indicates the number of logical<br>blocks to be copied. This is a 0’s based value.|||

35

**Figure 40: Copy – Source Range Entries Copy Descriptor Format 1h and Format 3h**

**Range**

**Bytes**

**Description**

23:22

**Source Options (SOPT): This field specifies options as follows:**

**Format**

**1h bits**

**Format**

**3h bits**

**Description**

n/a

**Fast Copy Only (FCO): If this bit is set to ‘1’, then the**
controller only performs fast copy operations (refer to section
3.3.2.1) for user data in this Source Range entry. If this bit is
cleared to ‘0’, then this bit has no effect.
15:00
14:00
Reserved
25:24
Reserved

35:26

**Expected Logical Block Tags (ELBT): This field specifies variable sized Expected**
Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag
(EILBRT) fields, which are defined in section 5.3.1.4.1, to be used for the read portion of
the copy operation. If the source namespace is not formatted to use end-to-end protection
information, then this field is ignored by the controller. Refer to section 5.3.

37:36

**Expected Logical Block Application Tag (ELBAT): This field specifies the Application**
Tag expected value used for the read portion of the copy operation for the LBAs specified
in this Source Range entry. If the source namespace is not formatted to use end-to-end
protection information, then this field is ignored by the controller. Refer to section 5.3.

39:38

**Expected Logical Block Application Tag Mask (ELBATM): This field specifies the**
Application Tag Mask expected value used for the read portion of the copy operation for
the LBAs specified in this Source Range entry. If the source namespace is not formatted
to use end-to-end protection information, then this field is ignored by the controller. Refer
to section 5.3.

Source
Range 1
43:40

**Source Parameters (SPARS)**
47:44
Reserved
55:48

**Starting LBA (SLBA)**
59:56

**Read Parameters (RPARS)**
61:60

**Command Extension Value (CEV)**
63:62

**Source Options (SOPT)**
65:64
Reserved
75:66

**Expected Logical Block Tags (ELBT): (i.e., ELBST and EILBRT)**
77:76

**Expected Logical Block Application Tag (ELBAT)**
79:78

**Expected Logical Block Application Tag Mask (ELBATM)**
…

Source
Range 101
4043:4040

**Source Parameters (SPARS)**
4047:4044
Reserved
4055:4048

**Starting LBA (SLBA)**
4059:4056

**Read Parameters (RPARS)**
4061:4060

**Command Extension Value (CEV)**
4063:4062

**Source Options (SOPT)**
4065:4064
Reserved
4075:4066

**Expected Logical Block Tags (ELBT) (i.e., ELBST and EILBRT)**
4077:4076

**Expected Logical Block Application Tag (ELBAT)**
4079:4078

**Expected Logical Block Application Tag Mask (ELBATM)**

The SNSID field (refer to Figure 40) specifies an active NSID that identifies the namespace for the source
range. If the SNSID field contains an invalid NSID, the value 0h, or the value FFFFFFFFh, then the controller
shall abort the Copy command with a status code of Invalid Namespace or Format. If the SNSID field
contains an inactive NSID, then the controller shall abort the Copy command with a status code of Invalid
Field in Command. If the SNSID field contains an active NSID that identifies a namespace that is not
comprised of logical blocks (refer to section 2.1), then the controller:


||Range|||Bytes|||Description||
|---|---|---|---|---|---|---|---|---|
||||23:22|||Source Options (SOPT): This field specifies options as follows:<br>Format Format<br>Description<br>1h bits 3h bits<br>Fast Copy Only (FCO): If this bit is set to ‘1’, then the<br>controller only performs fast copy operations (refer to section<br>n/a 15<br>3.3.2.1) for user data in this Source Range entry. If this bit is<br>cleared to ‘0’, then this bit has no effect.<br>15:00 14:00 Reserved|||
||||25:24|||Reserved|||
||||35:26|||Expected Logical Block Tags (ELBT): This field specifies variable sized Expected<br>Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag<br>(EILBRT) fields, which are defined in section 5.3.1.4.1, to be used for the read portion of<br>the copy operation. If the source namespace is not formatted to use end-to-end protection<br>information, then this field is ignored by the controller. Refer to section 5.3.|||
||||37:36|||Expected Logical Block Application Tag (ELBAT): This field specifies the Application<br>Tag expected value used for the read portion of the copy operation for the LBAs specified<br>in this Source Range entry. If the source namespace is not formatted to use end-to-end<br>protection information, then this field is ignored by the controller. Refer to section 5.3.|||
||||39:38|||Expected Logical Block Application Tag Mask (ELBATM): This field specifies the<br>Application Tag Mask expected value used for the read portion of the copy operation for<br>the LBAs specified in this Source Range entry. If the source namespace is not formatted<br>to use end-to-end protection information, then this field is ignored by the controller. Refer<br>to section 5.3.|||
||||||||||
|Source<br>Range 1|||43:40|||Source Parameters (SPARS)|||
||||47:44|||Reserved|||
||||55:48|||Starting LBA (SLBA)|||
||||59:56|||Read Parameters (RPARS)|||
||||61:60|||Command Extension Value (CEV)|||
||||63:62|||Source Options (SOPT)|||
||||65:64|||Reserved|||
||||75:66|||Expected Logical Block Tags (ELBT): (i.e., ELBST and EILBRT)|||
||||77:76|||Expected Logical Block Application Tag (ELBAT)|||
||||79:78|||Expected Logical Block Application Tag Mask (ELBATM)|||
||…||||||||
|Source<br>Range 101|||4043:4040|||Source Parameters (SPARS)|||
||||4047:4044|||Reserved|||
||||4055:4048|||Starting LBA (SLBA)|||
||||4059:4056|||Read Parameters (RPARS)|||
||||4061:4060|||Command Extension Value (CEV)|||
||||4063:4062|||Source Options (SOPT)|||
||||4065:4064|||Reserved|||
||||4075:4066|||Expected Logical Block Tags (ELBT) (i.e., ELBST and EILBRT)|||
||||4077:4076|||Expected Logical Block Application Tag (ELBAT)|||
||||4079:4078|||Expected Logical Block Application Tag Mask (ELBATM)|||


||Format|||Format||Description|
|---|---|---|---|---|---|---|
||1h bits|||3h bits|||
|n/a|||15|||Fast Copy Only (FCO): If this bit is set to ‘1’, then the<br>controller only performs fast copy operations (refer to section<br>3.3.2.1) for user data in this Source Range entry. If this bit is<br>cleared to ‘0’, then this bit has no effect.|
|15:00|||14:00|||Reserved|

36
•
shall abort the Copy command with one of the following three status codes:
o
Invalid Namespace or Format;
o
Incompatible Namespace or Format; or
o
Invalid Field in Command;
and
•
should use the Invalid Namespace or Format status code to abort that Copy command.
For a byte-based Copy Descriptor Format Type (i.e., 4h, refer to the Memory Copy command section of the

NSID that identifies the namespace for the source range. If the SNSID field contains an invalid NSID, the
value 0h, or the value FFFFFFFFh, then the controller shall abort the Copy command with a status code of
Invalid Namespace or Format. If the SNSID field contains an inactive NSID, then the controller shall abort
the Copy command with a status code of Invalid Field in Command. If the SNSID field contains an active
NSID that identifies a namespace that is not comprised of byte addressable memory (refer to the NVM
Express Subsystem Local Memory Command Set Specification), then the controller:
•
shall abort the Copy command with one of the following three status codes:
o
Invalid Namespace or Format;
o
Incompatible Namespace or Format; or
o
Invalid Field in Command;
and
•
should use the Invalid Namespace or Format status code to abort that Copy command.
If the number of Source Range entries (i.e., the value in the NR field) is greater than the value in the MSRC
field (refer to Figure 114), then the Copy command shall be aborted with a status code of Command Size
Limit Exceeded.
For an LBA-based Copy Descriptor Format Type (i.e., 0h, 1h, 2h, or 3h):
•
the number of logical blocks written by the Copy command is the sum of all Number of Logical
Blocks fields in all Source Range entries specified in the list of Source Range entries;
•
if a valid Source Range entry specifies a Number of Logical Blocks field that is greater than the
value in the MSSRL field (refer to Figure 114), then the Copy command shall be aborted with a
status code of Command Size Limit Exceeded; and
•
if the sum of all Number of Logical Blocks fields in all Source Range entries is greater than the
value in the MCL field (refer to Figure 114), then the Copy command shall be aborted with a status
code of Command Size Limit Exceeded.
For a byte-based Copy Descriptor Format Type (i.e., 4h):
•
the number of logical blocks written by the Copy command is determined by the sum of the Number
of Bytes fields (refer to the NVM Express Subsystem Local Memory Command Set Specification)
in all Source Range entries specified in the list of Source Range entries divided by the LBA Data
Size field (refer to Figure 115) of the LBA Format data structure associated with the destination
namespace);
•
if the sum of all Number of Bytes fields in all Source Range entries does not represent a multiple
of the LBA Data Size field of the destination namespace, then the Copy command shall be aborted
with a status code of Invalid Field in Command;
•
if a valid Source Range entry specifies a Number of Bytes field that represents a number of logical
blocks (i.e., as determined by the LBA Data Size field) that is greater than the value in the MSSRL
37
field (refer to Figure 114), then the Copy command shall be aborted with a status code of Command
Size Limit Exceeded; and
•
if the sum of all Number of Bytes fields in all Source Range entries represents a number of logical
blocks (i.e., as determined by the LBA Data Size field) that is greater than the value in the MCL
field (refer to Figure 114), then the Copy command shall be aborted with a status code of Command
Size Limit Exceeded.
The data bytes in the LBAs specified by each Source Range entry shall be copied to the destination LBA
range in the same order those LBAs are listed in the Source Range entries (e.g., the LBAs specified by
Source Range 0 are copied to the lowest numbered LBAs specified by the SDLBA field, the LBAs specified
by Source Range 1 are copied to the next consecutively numbered LBAs after the LBAs copied for Source
Range entry 0). The read operations and write operations used to perform the copy may operate
sequentially or in parallel.
The host should not specify a destination LBA range that overlaps the LBA in any of the Source Range
entries. If the host specifies a destination LBA range that overlaps with any LBAs specified in one or more
of the Source Range entries, then upon completion of the Copy command, the data stored in each logical
block in that overlapping destination LBA range may, within the constraints of the atomicity rules described
in section 2.1.4, be from any of the one or more Source Range entries in which that LBA is contained. This
is a result of the possibility that overlapping Source Range entries may be processed in any order.
Two LBA ranges overlap if they specify LBAs in the same namespace and there is at least one LBA that is
part of both LBA ranges.
For Source Range Entries Copy Descriptor Formats 0h and 1h, the host should not specify a destination
LBA range that overlaps the LBA in any of the Source Range entries. If the host specifies a destination LBA
range that overlaps with any LBAs specified in one or more of the Source Range entries, then upon
completion of the Copy command, the data stored in each logical block in that overlapping destination LBA
range may, within the constraints of the atomicity rules described in section 2.1.4, be from any of the one
or more Source Range entries in which that LBA is contained. This is a result of the possibility that
overlapping Source Range entries may be processed in any order.
For Source Range Entries Copy Descriptor Formats 2h and 3h, overlap of any source LBA range that is
located in the destination namespace with the destination LBA range is prohibited. If a Copy command
uses either Source Range Entries Copy Descriptor Format 2h or 3h and any specified source LBA range
that is located in the destination namespace has any LBAs in common with the specified destination LBA
range, then the controller shall abort the command with a status code of Overlapping I/O Range.
If the controller:
•
supports Reachability Reporting (refer to the Reachability Reporting architecture section in the

•
processes a Copy command that requests a copy between different namespaces (i.e., the NSID in
the SNSID field in a Source Range entry is different than the NSID of the destination namespace);
and
•
does not report a Reachability Association (refer to the Reachability Reporting architecture section
in the NVM Express Base Specification) between those namespaces,
then the controller shall abort the command with the status code set to Namespace Not Reachable.
If the read portion of a copy operation attempts to access a deallocated or unwritten logical block, the
controller shall operate as described in section 3.3.3.2.1.
38
Figure 41 shows an example of the relationship between the source LBAs and the destination LBAs.

**Figure 41: Source LBA and Destination LBA Relationship Example**

Range 3
215-224
Range 2
331-340
Range 0
101-150
Range 1
2300-2399
SDLBA + Sum (all NLB fields)
10001-10170
Destination LBAs:

Source LBAs:

**3.3.2.1**

**Fast copy operations**
A fast copy operation is a copy operation that uses a method that is expected to be no slower in total
elapsed time than the alternative of the host copying the user data by issuing Read commands and Write
commands. Unexpected NVM subsystem operating conditions (e.g., nature of concurrent I/O traffic,
availability of controller buffer space, errors, and failures) may cause individual copy operations to be slower
than host copying of the user data. High performance methods for fast copy operations include non-
read/write methods such as copy on write snapshot and copy on write clone and high-bandwidth copies
within a tightly integrated NVM subsystem such as an SSD.
A host is able to restrict a Copy command to only perform fast copy operations for user data specified by a
Source Range entry by setting the Fast Copy Only (FCO) bit to ‘1’ in that Source Range entry (refer to
Figure 39 and Figure 40). If the FCO bit is set to ‘1’ in a Source Range entry and the controller is unable to
use fast copy operations to copy the user data specified by that Source Range entry, then the controller
shall abort the command with a status code of Fast Copy Not Possible.
If the controller aborts a Copy command with a status code of Fast Copy Not Possible and clears the Do
Not Retry (DNR) bit to ‘0’ in the CQE for that command, then the host may retry that Copy command (e.g.,
by submitting that command to a different controller). If the controller aborts a Copy command with a status
code of Fast Copy Not Possible and sets the Do Not Retry (DNR) bit to ‘1’ in the CQE for that command,
then the host should not retry that Copy command (e.g., the host may submit Read commands and Write
commands to copy the user data).
A controller sets the NVM All Fast Copy (NVMAFC) bit to ‘1’ in the Optional NVM Command Support
(ONCS) field of the I/O Command Set Independent Identify Controller data structure (refer to the NVM
Express Base Specification) to indicate that for NVM Command Set Copy commands, all copy operations
are fast copy operations within the NVM subsystem that contains the controller. If all copy operations within
that NVM subsystem are fast copy operations, then the controller should set that bit to ‘1’.
39

**3.3.2.2**

**Copy atomicity**
If a controller:
•
complies with a version of the NVM Express NVM Command Set Specification later than revision
1.0;
•
complies with a version of the NVM Express Base Specification later than revision 2.0; or
•
supports the Copy command and either:
o
Source Range Entries Copy Descriptor Format 2h; or
o
Source Range Entries Copy Descriptor Format 3h,
then the controller shall set the NVM Copy Single Atomicity (NVMCSA) bit to ‘1’ in the ONCS field and shall
perform the write portion of a Copy command as a single write command to which the atomicity
requirements specified in section 2.1.4 apply.
In some situations, these atomicity requirements require the controller to process user data specified by a
portion of a Source Range entry as an atomic write operation, or to process user data specified by multiple
Source Range entries (and/or portions thereof) as an atomic write operation. For example, consider a
controller that is in Multiple Atomicity Mode for the destination namespace with an atomic write size of 8
logical blocks (e.g., as a consequence of the controller setting the NAWUN field to 8h in the Identify
Namespace data structure for the NVM Command Set (refer to Figure 114)):
•
if that controller processes a Copy command with 3 Source Ranges entries that each consist of 4
logical blocks and a destination LBA range that starts at an atomic boundary, then that controller
performs 2 atomic write operations, where the first atomic write operation consists of the 8 logical
blocks described by the first two Source Range entries and the second atomic write operation that
consists of the 4 logical blocks described by the third Source Range entry); and
•
if that controller processes a Copy command with 2 Source Ranges entries that each consist of 16
logical blocks and a destination LBA range that starts at an atomic boundary, then that controller
performs 4 atomic write operations, 2 atomic write operations for each Source Range entry where
each atomic write operation consists of half of the logical blocks described by a Source Range
entry.
A controller is able to limit the implementation impact of these atomicity requirements by reporting
appropriate values in the MSRC field, the MSSRL field, and the MCL field (refer to Figure 114).
If the NVMCSA bit in the ONCS field is cleared to ‘0’, then the controller is based on an older version of this
specification and the controller:
•
always performs the write portion of a Copy command that has a single Source Range entry as a
single write command to which the atomicity requirements specified in section 2.1.4 apply; and
•
may or may not perform the write portion of a Copy command that has more than one Source
Range entry as a separate write command for each Source Range entry. If the write portion of a
Copy command is performed as a separate write command for each Source Range entry, then an
independent instance of the atomicity requirements in section 2.1.4 applies to copying the user
data specified by each Source Range entry.
The value FFFFh for an atomicity parameter specified in section 2.1.4 (refer to Figure 4) indicates that the
atomicity of any write command is 10000h logical blocks. For write commands other than the Copy
command, that is the largest command size and hence indicates that the command is always atomic.
40
For a Copy command, 10000h logical blocks is not the largest command size and hence the value FFFFh
indicates only that the atomicity of the write portion of the Copy command is 10000h logical blocks. This
version of the NVM Command Set standard does not provide any means for a controller to indicate that the
write portion of all Copy commands is atomic.

**3.3.2.3**

**Copy within a Single Namespace**
This section applies to Copy commands that copy user data within a single namespace and use Source
Range Entries Copy Descriptor Format 0h or 1h. Refer to section 3.3.2.4 for Copy commands that use
Source Range Entries Copy Descriptor Format 2h or 3h.
If the single namespace that is the source namespace and the destination namespace for a Copy command
is formatted with protection information (PI), then the PRINFOR.PRACT bit and the PRINFOW.PRACT bit
in the Copy command affect the processing of PI as follows:
•
If the PRINFOR.PRACT bit and the PRINFOW.PRACT bit have the same value (i.e., both are set
to ‘1’ or both are cleared to ‘0’), then the controller shall perform the user data copying specified by
the Copy command for each Source Range entry with PI processed as specified in section
5.3.2.5.1; and
•
If the PRINFOR.PRACT bit and the PRINFOW.PRACT bit have different values (i.e., one bit is set
to ‘1’ and one bit is cleared to ‘0’) then the controller shall abort that Copy command with a status
code of Invalid Field in Command.
If the single namespace that is the source namespace and the destination namespace for a Copy command
is not formatted with PI, then the controller shall ignore the PRINFOR field and the PRINFOW field.

**3.3.2.4**

**Copy across Multiple Namespaces**
This section applies to Copy commands that use Source Range Entries Copy Descriptor Format 2h or 3h
to copy user data across multiple namespaces and/or within the same namespace. Refer to section 3.3.2.3
for Copy commands that use Source Range Entries Copy Descriptor Formats 0h or 1h.
A controller that supports copying user data across multiple logical block namespaces (i.e., namespaces
that use any I/O Command Set that specifies logical blocks) is able to use attached logical block
namespaces attached to the controller processing the command as a copy source or a copy destination.

**3.3.2.4.1**

**Matching and Corresponding Formats**
Copy command processing imposes restrictions on reformatting of logical block data and metadata that are
copied across different namespaces. For all copy source namespaces and the copy destination
namespace:
•
logical block data size is required to be the same;
•
metadata size is required to be the same, except that the copy destination namespace may have
a different metadata size if protection information (PI) metadata is inserted or stripped as part of
Copy command processing and all metadata is PI metadata; and
•
PI type and format settings are required to be the same unless PI is being inserted or stripped as
part of Copy command processing.
If the copy source namespaces and the copy destination namespace do not satisfy these restrictions, then
the Copy command is unable to copy user data among them. As an alternative, a host is able to use Read
commands and Write commands to copy user data via the host.
41
The specific restrictions are specified in section 3.3.2.4.2, which uses the following terms for formatting
restrictions on namespaces specified by a Copy command:
•

**matching namespace formats for copy: requirements that namespace format, PI type, and all**
other PI parameters for the namespaces be the same.
•

**corresponding protection information formats for copy (corresponding PI formats for copy):**
requirements that the namespace formats differ only by the presence or absence of PI.
The specific requirements for each of these terms are specified in the remainder of this section.
Multiple namespaces that are formatted with PI have matching namespace formats for copy if each
namespace uses the NVM Command Set or any other command set that both specifies logical blocks and
includes the Copy command specified for the NVM Command Set (e.g., the Zoned Namespace Command
Set) and all of the namespaces:
•
are formatted with the same logical block data size;
•
are formatted with the same metadata size; and
•
have the same value for each of the following:
o
the End-to-end Data Protection Type Settings (DPS) field in the Identify Namespace data
structure (refer to Figure 114);
o
the Protection Information Format Attribute (PIFA) field in the NVM Command Set I/O
Command Set specific Identify Namespace data structure (refer to Figure 118);
o
the bits in the Logical Block Storage Tag Mask (LBSTM) field in the NVM Command Set
I/O Command Set specific Identify Namespace data structure (refer to Figure 118) that are
not ignored by the host; and
o
the following fields in the extended LBA format (refer to Figure 119) that was used to format
the namespace:
▪
the Protection Information Format (PIF) field;
▪
the Qualified Protection Information Format (QPIF) if the PIF field is set to 11b (i.e.,
Qualified Type); and
▪
the Storage Tag Size (STS) field.
Multiple namespaces that are formatted without PI have matching namespace formats for copy if each
namespace uses the NVM Command Set or any other I/O Command Set that both specifies logical blocks
and includes the Copy command specified for the NVM Command Set (e.g., the Zoned Namespace
Command Set) and all of the namespaces are formatted with both the same logical block data size and the
same metadata size.
Multiple namespaces where at least one of the namespaces is formatted with PI and at least one of the
namespaces is formatted without PI do not have matching namespace formats for copy.
A namespace that is formatted with PI and a namespace that is formatted without PI have corresponding
PI formats for copy if:
•
each namespace uses either the NVM Command Set or any other I/O Command Set that both
specifies logical blocks and includes the Copy command specified for the NVM Command Set (e.g.,
the Zoned Namespace Command Set);
•
both namespaces are formatted with the same logical block data size;
•
the namespace that is formatted with PI is formatted with metadata size equal to PI size (refer to
section 5.3.1) (i.e., does not contain any metadata other than PI); and
42
•
the namespace that is formatted without PI is also formatted without any metadata.
A namespace that is formatted with any metadata that is not PI metadata does not have a corresponding
PI format for copy with any other namespace.

**3.3.2.4.2**

**Handling of Protection Information**
Protection information (PI) and data copying functionality depends on the formats of the source and
destination namespaces, the value of the PRINFOR.PRACT bit in the Copy command, and the value of the
PRINFOW.PRACT bit in the Copy command as applicable. This functionality is specified for each Source
Range entry, as the controller may process Source Range entries concurrently and in any order provided
that all Copy command requirements (e.g., atomicity) are satisfied.
If the source namespace for Source Range 0 is formatted without PI, and the destination namespace is
formatted without PI, then for each Source Range entry, including Source Range 0:
•
if the source namespace for that Source Range entry and the destination namespace have
matching namespace formats for copy, then the controller shall perform the user data copying
specified by the Copy command for that Source Range entry; and
•
if the source namespace for that Source Range entry and the destination namespace do not have
matching namespace formats for copy, then the controller:
o
shall not copy any user data specified by that Source Range entry; and
o
shall abort the command with a status code of Incompatible Namespace or Format.
If the source namespace for Source Range 0 is formatted with PI, the destination namespace is formatted
with PI, the PRINFOR.PRACT bit is cleared to ‘0’, and the PRINFOW.PRACT bit is cleared to ‘0’, then for
each Source Range entry, including Source Range 0:
•
if the source namespace for that Source Range entry and the destination namespace have
matching namespace formats for copy, then the controller shall perform the user data copying
specified by the Copy command for that Source Range entry with PI passed through as specified
in section 5.3.2.5.2; and
•
if the source namespace for that Source Range entry and the destination namespace do not have
matching namespace formats for copy, then the controller:
o
shall not copy any user data specified by that Source Range entry; and
o
shall abort the command with a status code of Incompatible Namespace or Format.
If the source namespace for Source Range 0 is formatted with PI, the destination namespace is formatted
with PI, the PRINFOR.PRACT bit is set to ‘1’ and the PRINFOW.PRACT bit is set to ‘1’, then for each
Source Range entry, including Source Range 0:
•
if the source namespace for that Source Range entry and the destination namespace have
matching namespace formats for copy, then the controller shall perform the user data copying
specified by the Copy command for that Source Range entry with PI replaced as specified in section
5.3.2.5.2; and
•
if the source namespace for that Source Range entry and the destination namespace do not have
matching namespace formats for copy, then the controller:
o
shall not copy any user data specified by that Source Range entry; and
o
shall abort the command with a status code of Incompatible Namespace or Format.
43
If the source namespace for Source Range 0 is formatted with PI, the destination namespace is formatted
with PI, and the PRINFOR.PRACT bit has a different value from the PRINFOW.PRACT bit, then the
controller shall abort the command with a status code of Invalid Field in Command.
If the source namespace for Source Range 0 is formatted without PI, the destination namespace is
formatted with PI, and the PRINFOW.PRACT bit is set to ‘1’, then for each Source Range entry, including
Source Range 0:
•
if the source namespace for that Source Range entry is formatted without PI and has a
corresponding PI format for copy with the destination namespace, then the controller shall perform
the user data copying specified by the Copy command for that Source Range entry with PI inserted
as specified in section 5.3.2.5.2; and
•
if the source namespace for that Source Range entry is formatted with PI or does not have a
corresponding PI format for copy with the destination namespace, then the controller:
o
shall not copy any user data specified by that Source Range entry; and
o
shall abort the command with a status code of Incompatible Namespace or Format.
If the source namespace for Source Range 0 is formatted without PI, the destination namespace is
formatted with PI, and the PRINFOW.PRACT bit is cleared to ‘0’, then the controller shall abort the
command with a status code of Incompatible Namespace or Format.
If the source namespace for Source Range 0 is formatted with PI, the destination namespace is formatted
without PI, and the PRINFOR.PRACT bit is set to ‘1’, then for each Source Range entry, including Source
Range 0:
•
if the source namespace for that Source Range entry is formatted with PI and has a corresponding
PI format for copy with the destination namespace, then the controller shall perform the data
copying specified by the Copy command for that Source Range entry with PI stripped as specified
in section 5.3.2.5.2; and
•
if the source namespace for that Source Range entry is not formatted with PI or does not have a
corresponding PI format for copy with the destination namespace, then the controller:
o
shall not copy any user data specified by that Source Range entry; and
o
shall abort the command with a status code of Incompatible Namespace or Format.
If the source namespace for Source Range 0 is formatted with PI, the destination namespace is formatted
without PI, and the PRINFOR.PRACT bit is cleared to ‘0’, then the controller shall abort the command with
a status code of Incompatible Namespace or Format.

**3.3.2.5**

**Command Completion**
When the command is completed, the controller shall post a completion queue entry to the associated I/O
Completion Queue indicating the status for the command.
If the command completes with failure (i.e., completes with a status code other than Successful
Completion), then:
•
the controller may or may not have copied some of the user data;
•
Dword 0 of the completion queue entry contains the number of the lowest numbered Source Range
entry that was not successfully copied (e.g., if Source Range 0, Source Range 1, Source Range 2,
and Source Range 5 are copied successfully and Source Range 3 and Source Range 4 are not
copied successfully, then Dword 0 is set to 3); and
44
•
prior to aborting the command, the controller may or may not have copied some (or all) of the data
specified by that Copy command for the Source Range entries that have a number greater than or
equal to the value in Dword 0.
If no data was written to the destination LBAs, then Dword 0 of the completion queue entry shall be cleared
to 0h.
Copy command specific errors are defined in Figure 42.

**Figure 42: Copy – Command Specific Status Values**

**Value**

**Definition**

81h
Invalid Protection Information: The protection information specified by the command is invalid due to:
•
The Protection Information Read (PRINFOR) field or Protection Information Write (PRINFOW) field
(refer to Figure 34) containing an invalid value for the Protection Information with which the
namespace was formatted (refer to the PI field in the Format NVM Command section in the NVM
Express Base Specification and the DPS field in Figure 114);
•
the ILBRT field being invalid (refer to section 5.3.3); or
•
the EILBRT field in a Source Range entry being invalid (refer to section 5.3.3).

82h

**Attempted Write to Read Only Range: The destination LBA range specified contains read-only blocks.**
The controller shall not return this status value if the read-only condition on the media is a result of a change
in the write protection state of a namespace (refer to the Namespace Write Protection section in the NVM

**Express Base Specification).**
83h
Command Size Limit Exceeded: One or more of the Copy command processing limits (i.e., non-zero value
of the NR, MSSRL, and MCL fields in the Identify Namespace data structure) was exceeded.
85h

**Incompatible Namespace or Format: At least one source namespace and the destination namespace**

**have incompatible formats (refer to section 3.3.2.4).**
86h

**Fast Copy Not Possible: The Fast Copy Only (FCO) bit was set to ‘1’ in a Source Range entry and the**
controller was not able to use fast copy operations to copy the specified data (refer to section 3.3.2.1).
87h
Overlapping I/O Range: A source logical block range overlaps the destination logical block range (refer to

**section 3.3.2).**

88h

**Namespace Not Reachable: One or more of the Source Range entries specifies the NSID of a namespace**
that is not contained in any Reachability Group that is in a Reachability Association with the Reachability
Group that contains the destination namespace. Refer to the Reachability Reporting architecture section in

**the NVM Express Base Specification.**
89h
Insufficient Resources: A resource shortage prevented the controller from performing the requested copy.
The host should not retry the command on the same controller.

**Dataset Management command**
The Dataset Management command is used by the host to indicate attributes for ranges of logical blocks.
This includes attributes like frequency that data is read or written, access size, and other information that
may be used to optimize performance and reliability. This command is advisory; a compliant controller may
choose to take no action based on information provided.
The command uses Command Dword 10, and Command Dword 11 fields. If the command uses PRPs for
the data transfer, then the PRP Entry 1 and PRP Entry 2 fields are used. If the command uses SGLs for
the data transfer, then the SGL Entry 1 field is used. All other command specific fields are reserved.

**Figure 43: Dataset Management – Data Pointer**

**Bits**

**Description**
127:00

**Data Pointer (DPTR): This field specifies the data to use for the command. Refer to the Common**
Command Format figure in the NVM Express Base Specification for the definition of this field.


||Value|||Definition||
|---|---|---|---|---|---|
|81h|||Invalid Protection Information: The protection information specified by the command is invalid due to:<br>• The Protection Information Read (PRINFOR) field or Protection Information Write (PRINFOW) field<br>(refer to Figure 34) containing an invalid value for the Protection Information with which the<br>namespace was formatted (refer to the PI field in the Format NVM Command section in the NVM<br>Express Base Specification and the DPS field in Figure 114);<br>• the ILBRT field being invalid (refer to section 5.3.3); or<br>• the EILBRT field in a Source Range entry being invalid (refer to section 5.3.3).|||
|82h|||Attempted Write to Read Only Range: The destination LBA range specified contains read-only blocks.<br>The controller shall not return this status value if the read-only condition on the media is a result of a change<br>in the write protection state of a namespace (refer to the Namespace Write Protection section in the NVM<br>Express Base Specification).|||
|83h|||Command Size Limit Exceeded: One or more of the Copy command processing limits (i.e., non-zero value<br>of the NR, MSSRL, and MCL fields in the Identify Namespace data structure) was exceeded.|||
|85h|||Incompatible Namespace or Format: At least one source namespace and the destination namespace<br>have incompatible formats (refer to section 3.3.2.4).|||
|86h|||Fast Copy Not Possible: The Fast Copy Only (FCO) bit was set to ‘1’ in a Source Range entry and the<br>controller was not able to use fast copy operations to copy the specified data (refer to section 3.3.2.1).|||
|87h|||Overlapping I/O Range: A source logical block range overlaps the destination logical block range (refer to<br>section 3.3.2).|||
|88h|||Namespace Not Reachable: One or more of the Source Range entries specifies the NSID of a namespace<br>that is not contained in any Reachability Group that is in a Reachability Association with the Reachability<br>Group that contains the destination namespace. Refer to the Reachability Reporting architecture section in<br>the NVM Express Base Specification.|||
|89h|||Insufficient Resources: A resource shortage prevented the controller from performing the requested copy.<br>The host should not retry the command on the same controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|127:00|||Data Pointer (DPTR): This field specifies the data to use for the command. Refer to the Common<br>Command Format figure in the NVM Express Base Specification for the definition of this field.|||

45

**Figure 44: Dataset Management – Command Dword 10**

**Bits**

**Description**
31:08
Reserved
07:00
Number of Ranges (NR): Indicates the number of 16 byte range sets that are specified in the command.
This is a 0’s based value.

**Figure 45: Dataset Management – Command Dword 11**

**Bits**

**Description**
31:03
Reserved
Attribute – Deallocate (AD): If this bit is set to ‘1’, then the NVM subsystem may deallocate all provided
ranges. The data returned for logical blocks that were deallocated is specified in section 3.3.3.2.1. The
data and metadata for logical blocks that are not deallocated by the NVM subsystem are not changed

**as the result of a Dataset Management command.**
Attribute – Integral Dataset for Write (IDW): If this bit is set to ‘1’, then the dataset should be optimized
for write access as an integral unit. The host expects to perform operations on all ranges provided as an
integral unit for writes, indicating that if a portion of the dataset is written then it is expected that all of the

**ranges in the dataset are going to be written by the host.**
Attribute – Integral Dataset for Read (IDR): If this bit is set to ‘1’, then the dataset should be optimized
for read access as an integral unit. The host expects to perform operations on all ranges provided as an
integral unit for reads, indicating that if a portion of the dataset is read then it is expected that all of the

**ranges in the dataset are going to be read by the host.**

If the Dataset Management command is supported, all combinations of attributes specified in Figure 45
may be set.
The data that the Dataset Management command provides is a list of ranges with context attributes. Each
range consists of a starting LBA, a length of logical blocks that the range consists of and the context
attributes to be applied to that range. The Length in Logical Blocks field is a 1-based value. The definition
of the Dataset Management command Range field is specified in Figure 46. The maximum case of 256
ranges is shown.

**Figure 46: Dataset Management – Range Definition**

**Range**

**Bytes**

**Field**

Range 0
03:00

**Context Attributes (CATTR)**
07:04

**Length in Logical Blocks (LLB)**
15:08

**Starting LBA (SLBA)**

Range 1
19:16

**Context Attributes (CATTR)**
23:20

**Length in Logical Blocks (LLB)**
31:24

**Starting LBA (SLBA)**
…

Range 255
4083:4080

**Context Attributes (CATTR)**
4087:4084

**Length in Logical Blocks (LLB)**
4095:4088

**Starting LBA (SLBA)**


||Bits|||Description||
|---|---|---|---|---|---|
|31:08|||Reserved|||
|07:00|||Number of Ranges (NR): Indicates the number of 16 byte range sets that are specified in the command.<br>This is a 0’s based value.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:03|||Reserved|||
|02|||Attribute – Deallocate (AD): If this bit is set to ‘1’, then the NVM subsystem may deallocate all provided<br>ranges. The data returned for logical blocks that were deallocated is specified in section 3.3.3.2.1. The<br>data and metadata for logical blocks that are not deallocated by the NVM subsystem are not changed<br>as the result of a Dataset Management command.|||
|01|||Attribute – Integral Dataset for Write (IDW): If this bit is set to ‘1’, then the dataset should be optimized<br>for write access as an integral unit. The host expects to perform operations on all ranges provided as an<br>integral unit for writes, indicating that if a portion of the dataset is written then it is expected that all of the<br>ranges in the dataset are going to be written by the host.|||
|00|||Attribute – Integral Dataset for Read (IDR): If this bit is set to ‘1’, then the dataset should be optimized<br>for read access as an integral unit. The host expects to perform operations on all ranges provided as an<br>integral unit for reads, indicating that if a portion of the dataset is read then it is expected that all of the<br>ranges in the dataset are going to be read by the host.|||


||Range|||Bytes|||Field||
|---|---|---|---|---|---|---|---|---|
||||||||||
|Range 0|||03:00|||Context Attributes (CATTR)|||
||||07:04|||Length in Logical Blocks (LLB)|||
||||15:08|||Starting LBA (SLBA)|||
||||||||||
|Range 1|||19:16|||Context Attributes (CATTR)|||
||||23:20|||Length in Logical Blocks (LLB)|||
||||31:24|||Starting LBA (SLBA)|||
||…||||||||
||||||||||
|Range 255|||4083:4080|||Context Attributes (CATTR)|||
||||4087:4084|||Length in Logical Blocks (LLB)|||
||||4095:4088|||Starting LBA (SLBA)|||

46

**3.3.3.1**

**Dataset Management Processing Limits**
Processing limits for Dataset Management commands are indicated by non-zero values in three fields in
the I/O Command Set specific Identify Controller data structure (refer to Figure 120):
a) A non-zero value in the Dataset Management Ranges Limit (DMRL) field indicates a processing
limit on the number of ranges. If the controller reports a non-zero value in this field, then the
controller does not process attributes and context attributes for any range whose range number
(i.e., the number of the range as specified in the Range column of Figure 46) is greater than or
equal to that non-zero value.
b) A non-zero value in the Dataset Management Range Size Limit (DMRSL) field indicates a
processing limit on the number of logical blocks in a single range. If the controller reports a non-
zero value in this field, then the controller does not process attributes and context attributes for any
logical block whose LBA offset from the starting LBA of the range (refer to Figure 46) that specifies
the logical block is greater than or equal to that non-zero value.
c) A non-zero value in the Dataset Management Size Limit (DMSL) field indicates a processing limit
on the total number of logical blocks for the command. If the controller reports a non-zero value in
this field, then the controller does not process attributes and context attributes for any logical block
specified by any range for which the sum of:
a. the number of logical blocks, specified by lower numbered ranges, if any, otherwise zero;
and
b. the LBA offset for that logical block from the starting LBA of that range,
is greater than or equal to that non-zero value.
A logical block specified by a Dataset Management command satisfies all three of these processing limits
if and only if each processing limit does not prevent controller processing of attributes and context attributes
for that logical block. A logical block specified by a Dataset Management command does not satisfy a
processing limit if that limit prevents controller processing of attributes and context attributes for that logical
block.
The controller shall set all three processing limit fields (i.e., the DMRL, DMRSL and DMSL fields) to non-
zero values or shall clear all three processing limit fields to 0h. A controller is able to impose a subset of
the three processing limits by setting the field that reports each unused processing limit to the maximum
possible value for that field (i.e., all bits set to ‘1’), with the exception that the resulting processing limit for
the number of ranges is 255 of the 256 ranges supported by the Dataset Management command. Note that
this exception is due to the DMRL field being 1-based in contrast to the 0’s-based Number of Ranges (NR)
field in the Dataset Management command.
If all three processing limit fields (i.e., the DMRL, DMRSL and DMSL fields) contain non-zero values, then
the controller supports the Dataset Management command and:
a) Each processing limit field indicates a processing limit for controller processing of attributes and
context attributes for logical blocks specified by the command;
b) If Dataset Management Support Variants (NVMDSMSV) bit is set to ‘1’ in the Optional NVM
Command Support (ONCS) field in the Identify Controller data structure, then for the logical blocks
specified by the command:
a. The controller should process attributes and context attributes for all logical blocks that
satisfy all three processing limits; and
b. The controller should not process attributes and context attributes for any logical blocks
that do not satisfy one or more of the three processing limits;
and
c) If the NVMDSMSV bit is cleared to ‘0’, then for the logical blocks specified by the command:
47
a. If all logical blocks specified by the command satisfy all three processing limits, then the
controller shall process attributes and context attributes for those logical blocks; and
b. If the command specifies any logical block that does not satisfy one or more of the three
processing limits, then the controller shall abort the command with Command Size Limit
Exceeded status.
If all three processing limit fields (i.e., the DMRL, DMRSL and DMSL fields) are cleared to 0h then:
a) If the NVMDSMSV bit is set to ‘1’, then the controller supports the Dataset Management command
and does not report any processing limits on the number of ranges, number of logical blocks in a
single range or total number of logical blocks for the command; and
b) If the NVMDSMSV bit is cleared to ‘0’, then the controller does not support the Dataset
Management command.
A controller may choose to take no action on any or all logical blocks for which attributes or context attributes
are processed. If a Dataset Management command contains one or more ranges for which neither attributes
nor context attributes are processed, then a controller may nonetheless check the fields that specify such
ranges and abort the command if an error is detected (e.g., if the controller detects that such a range
extends beyond the size of the namespace).

**3.3.3.1.1**

**Dataset Management Processing Limits Example**
For example, under the assumptions that the Dataset Management Support Variants (NVMDSMSV) bit is
set to ‘1’ in the ONCS field and the DMRSL field is set to its maximum value, consider a Dataset
Management command that specifies two ranges, with range 0 containing 1,024 logical blocks and range
1 containing 512 logical blocks:
a) if the DMRL field is set to 1 and the DMSL field is set to 1,048, then the controller is expected to
process attributes and context attributes for the logical blocks specified by range 0, and the
controller does not process either attributes or context attributes for the logical blocks contained in
range 1; and
b) if the DMRL field is set to 2 and the DMSL field is set to 1,048, then the controller is expected to
process attributes and context attributes for the logical blocks specified by range 0 and for the first
24 logical blocks of range 1, and the controller does not process either attributes or context
attributes for the other logical blocks (i.e., 25 - 512) contained in range 1.

**3.3.3.2**

**Context Attributes**
The context attributes specified for each range provides information about how the range is intended to be
used by the host. The use of this information is optional and the controller is not required to perform any
specific action.
Note: The controller is required to maintain the integrity of data on the NVM media regardless of whether
the attributes provided by the host are accurate.

**Figure 47: Dataset Management – Context Attributes**

**Bits**

**Description**

31:24

**Command Access Size (CASZE): This field is the number of logical blocks expected to be transferred**
in a single Read or Write command from this dataset. A value of 0h indicates no Command Access Size
is provided.
23:11
Reserved
Write Prepare (WPREP): If this bit is set to ‘1’, then the provided range is expected to be written in the
near future.
Sequential Write Range (SWR): If this bit is set to ‘1’, then the dataset should be optimized for sequential
write access. The host expects to perform operations on the dataset as a single object for writes.


||Bits|||Description||
|---|---|---|---|---|---|
|31:24|||Command Access Size (CASZE): This field is the number of logical blocks expected to be transferred<br>in a single Read or Write command from this dataset. A value of 0h indicates no Command Access Size<br>is provided.|||
|23:11|||Reserved|||
|10|||Write Prepare (WPREP): If this bit is set to ‘1’, then the provided range is expected to be written in the<br>near future.|||
|09|||Sequential Write Range (SWR): If this bit is set to ‘1’, then the dataset should be optimized for sequential<br>write access. The host expects to perform operations on the dataset as a single object for writes.|||

48

**Figure 47: Dataset Management – Context Attributes**

**Bits**

**Description**
Sequential Read Range (SRR): If this bit is set to ‘1’, then the dataset should be optimized for sequential
read access. The host expects to perform operations on the dataset as a single object for reads.
07:06
Reserved

05:04

**Access Latency (AL): This field specifies the expected access latency.**

**Value**

**Definition**
00b
None. No latency information provided.
01b
Idle. Longer latency acceptable.
10b
Normal. Typical latency.
11b
Low. Smallest possible latency.

03:00

**Access Frequency (AF): This field specifies the expected access frequency.**

**Value**

**Definition**
0h
No frequency information provided.
1h
Typical number of reads and writes expected for this LBA range.
2h
Infrequent writes and infrequent reads to the LBA range indicated.
3h
Infrequent writes and frequent reads to the LBA range indicated.
4h
Frequent writes and infrequent reads to the LBA range indicated.
5h
Frequent writes and frequent reads to the LBA range indicated.
6h to Fh
Reserved

**3.3.3.2.1**

**Deallocated or Unwritten Logical Blocks**
A logical block that has never been written to, or which has been deallocated using the Dataset
Management command, the Write Zeroes command or the Sanitize command is called a deallocated or
unwritten logical block.
Using the Error Recovery feature (refer to section 4.1.3.2), the host may select the behavior of the controller
when reading deallocated or unwritten blocks. The controller shall abort Copy, Read, Verify, or Compare
commands that include deallocated or unwritten blocks with a status code of Deallocated or Unwritten
Logical Block if that error has been enabled using the DULBE bit in the Error Recovery feature. If the
Deallocated or Unwritten Logical Block error is not enabled, the values read from a deallocated or unwritten
block and its metadata (excluding protection information) shall be:
•
all bytes cleared to 0h if the Deallocation Read Behavior (DRB) field in the DLFEAT field is set to
001b;
•
all bytes set to FFh if the DRB field is set to 010b; or
•
either all bytes cleared to 0h or all bytes set to FFh if the DRB field is cleared to 000b.
The value read from a deallocated logical block shall be deterministic; specifically, the value returned by
subsequent reads of that logical block shall be the same until a write operation occurs to that logical block.
A deallocated or unwritten block is no longer deallocated or unwritten when the logical block is written.

**Read operations and Verify operations do not affect the deallocation status of a logical block.**
The values read from a deallocated or unwritten logical block’s protection information field shall:
•
have each byte in the Guard field value set to FFh or set to the CRC for the value read from the
deallocated logical block and its metadata (excluding protection information) (e.g., cleared to 0h if
the value read is all bytes cleared to 0h); and
•
have each byte in the Storage Tag field (if defined), the Application Tag field, and the Logical Block
Reference Tag field set to FFh (indicating the protection information shall not be checked).
Using the Error Recovery feature (refer to section 4.1.3.2), the host may enable an error to be returned if a
deallocated or unwritten logical block is read. If this error is supported for the namespace and enabled, then


||Bits|||Description||
|---|---|---|---|---|---|
|08|||Sequential Read Range (SRR): If this bit is set to ‘1’, then the dataset should be optimized for sequential<br>read access. The host expects to perform operations on the dataset as a single object for reads.|||
|07:06|||Reserved|||
|05:04|||Access Latency (AL): This field specifies the expected access latency.<br>Value Definition<br>00b None. No latency information provided.<br>01b Idle. Longer latency acceptable.<br>10b Normal. Typical latency.<br>11b Low. Smallest possible latency.|||
|03:00|||Access Frequency (AF): This field specifies the expected access frequency.<br>Value Definition<br>0h No frequency information provided.<br>1h Typical number of reads and writes expected for this LBA range.<br>2h Infrequent writes and infrequent reads to the LBA range indicated.<br>3h Infrequent writes and frequent reads to the LBA range indicated.<br>4h Frequent writes and infrequent reads to the LBA range indicated.<br>5h Frequent writes and frequent reads to the LBA range indicated.<br>6h to Fh Reserved|||


||Value|||Definition||
|---|---|---|---|---|---|
|00b|||None. No latency information provided.|||
|01b|||Idle. Longer latency acceptable.|||
|10b|||Normal. Typical latency.|||
|11b|||Low. Smallest possible latency.|||


||Value|||Definition||
|---|---|---|---|---|---|
|0h|||No frequency information provided.|||
|1h|||Typical number of reads and writes expected for this LBA range.|||
|2h|||Infrequent writes and infrequent reads to the LBA range indicated.|||
|3h|||Infrequent writes and frequent reads to the LBA range indicated.|||
|4h|||Frequent writes and infrequent reads to the LBA range indicated.|||
|5h|||Frequent writes and frequent reads to the LBA range indicated.|||
|6h to Fh|||Reserved|||

49
any User Data Read Access Command that includes a deallocated or unwritten logical block shall abort
with the Deallocated or Unwritten Logical Block status code. Note: Legacy software may not handle an
error for this case.
Note: The operation of the Deallocate function is similar to the ATA DATA SET MANAGEMENT with Trim
feature described in ACS-5 and SCSI UNMAP command described in SBC-4.

**3.3.3.3**

**Command Completion**
When the command is completed, the controller shall post a completion queue entry to the associated I/O
Completion Queue indicating the status for the command.
Dataset Management command specific status values (i.e., SCT field set to 1h) are shown in Figure 48.

**Figure 48: Dataset Management – Command Specific Status Values**

**Value**

**Definition**
80h

**Conflicting Attributes: The attributes specified in the command are conflicting.**

82h
Attempted Write to Read Only Range: The controller may optionally report this status if a Deallocate is
attempted for a read only range. The controller shall not return this status value if the read-only condition
on the media is a result of a change in the write protection state of a namespace (refer to the Namespace

**Write Protection section in the NVM Express Base Specification).**

83h

**Command Size Limit Exceeded: One or more of the Dataset Management processing limits (i.e., non-**
zero values of the DMRL, DMRSL and DMSL fields in the Identify Controller data structure) was exceeded
(refer to section 3.3.3.1). The controller shall not return this status value if the Dataset Management Support
Variants (NVMDSMSV) bit is set to ‘1’ in the Optional NVM Command Support field in the Identify Controller

**data structure.**

**Read command**
The Read command reads data and metadata, if applicable, from the I/O controller for the LBAs indicated.
The command may specify protection information to be checked as part of the read operation.
The command uses Command Dword 2, Command Dword 3, Command Dword 10, Command Dword 11,
Command Dword 12, Command Dword 13, Command Dword 14, and Command Dword 15 fields. If the
command uses PRPs for the data transfer, then the Metadata Pointer, PRP Entry 1, and PRP Entry 2 fields
are used. If the command uses SGLs for the data transfer, then the Metadata SGL Segment Pointer and
SGL Entry 1 fields are used.

**Figure 49: Read – Metadata Pointer**

**Bits**

**Description**
63:00
Metadata Pointer (MPTR): This field contains the Metadata Pointer, if applicable. Refer to the Common
Command Format figure in the NVM Express Base Specification for the definition of this field.

**Figure 50: Read – Data Pointer**

**Bits**

**Description**
127:00

**Data Pointer (DPTR): This field specifies where data is transferred to. Refer to the Common Command**
Format figure in the NVM Express Base Specification for the definition of this field.

**Figure 51: Read – Command Dword 2 and Dword 3**

**Bits**

**Description**
63:48
Reserved


||Value|||Definition||
|---|---|---|---|---|---|
|80h|||Conflicting Attributes: The attributes specified in the command are conflicting.|||
|82h|||Attempted Write to Read Only Range: The controller may optionally report this status if a Deallocate is<br>attempted for a read only range. The controller shall not return this status value if the read-only condition<br>on the media is a result of a change in the write protection state of a namespace (refer to the Namespace<br>Write Protection section in the NVM Express Base Specification).|||
|83h|||Command Size Limit Exceeded: One or more of the Dataset Management processing limits (i.e., non-<br>zero values of the DMRL, DMRSL and DMSL fields in the Identify Controller data structure) was exceeded<br>(refer to section 3.3.3.1). The controller shall not return this status value if the Dataset Management Support<br>Variants (NVMDSMSV) bit is set to ‘1’ in the Optional NVM Command Support field in the Identify Controller<br>data structure.|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:00|||Metadata Pointer (MPTR): This field contains the Metadata Pointer, if applicable. Refer to the Common<br>Command Format figure in the NVM Express Base Specification for the definition of this field.|||


||Bits|||Description||
|---|---|---|---|---|---|
|127:00|||Data Pointer (DPTR): This field specifies where data is transferred to. Refer to the Common Command<br>Format figure in the NVM Express Base Specification for the definition of this field.|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:48|||Reserved|||
|||||||

50

**Figure 51: Read – Command Dword 2 and Dword 3**

**Bits**

**Description**

47:00

**Expected Logical Block Tags Upper (ELBTU): This field and Command Dword 14 specify the variable**
sized Expected Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag
(EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-
end protection information, then this field is ignored by the controller.

**Figure 52: Read – Command Dword 10 and Command Dword 11**

**Bits**

**Description**
63:00
Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block to be read as part
of the operation. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits 63: 32.

**Figure 53: Read – Command Dword 12**

**Bits**

**Description**
Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this bit
is cleared to ‘0’, then the controller should apply all available error recovery means to return the data to
the host.
Force Unit Access (FUA): If this bit is set to ‘1’, then for data and metadata, if any, associated with
logical blocks specified by the Read command, the controller shall:
1)
commit that data and metadata, if any, to non-volatile medium; and
2)
return the data, and metadata, if any, that are read from non-volatile medium.
There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has no effect.
29:26

**Protection Information (PRINFO): Specifies the protection information action and check field, as**

**defined in Figure 11.**
Reserved
Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of end-to-
end data protection processing as defined in Figure 12.
23:20
Reserved
19:16

**Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the**
command (refer to the Key Per I/O section in the NVM Express Base Specification).
15:00
Number of Logical Blocks (NLB): This field indicates the number of logical blocks to be read. This is a

**0’s based value.**

The definition of Command Dword 13 is based on the CETYPE value. If the CETYPE value is cleared to
0h, then Command Dword 13 is defined in Figure 54. If the CETYPE value is non-zero, then Command
Dword 13 is defined in Figure 55.

**Figure 54: Read – Command Dword 13 if CETYPE is cleared to 0h**

**Bits**

**Description**
31:08
Reserved


||Bits|||Description||
|---|---|---|---|---|---|
|47:00|||Expected Logical Block Tags Upper (ELBTU): This field and Command Dword 14 specify the variable<br>sized Expected Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag<br>(EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-<br>end protection information, then this field is ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:00|||Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block to be read as part<br>of the operation. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits 63: 32.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31|||Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this bit<br>is cleared to ‘0’, then the controller should apply all available error recovery means to return the data to<br>the host.|||
|30|||Force Unit Access (FUA): If this bit is set to ‘1’, then for data and metadata, if any, associated with<br>logical blocks specified by the Read command, the controller shall:<br>1) commit that data and metadata, if any, to non-volatile medium; and<br>2) return the data, and metadata, if any, that are read from non-volatile medium.<br>There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has no effect.|||
|29:26|||Protection Information (PRINFO): Specifies the protection information action and check field, as<br>defined in Figure 11.|||
|25|||Reserved|||
|24|||Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of end-to-<br>end data protection processing as defined in Figure 12.|||
|23:20|||Reserved|||
|19:16|||Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the<br>command (refer to the Key Per I/O section in the NVM Express Base Specification).|||
|15:00|||Number of Logical Blocks (NLB): This field indicates the number of logical blocks to be read. This is a<br>0’s based value.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:08|||Reserved|||

51

**Figure 54: Read – Command Dword 13 if CETYPE is cleared to 0h**

**Bits**

**Description**

07:00

**Dataset Management (DSM): This field indicates attributes for the LBA(s) being read.**

**Bits**

**Description**

**Incompressible (INCPRS): If this bit is set to ‘1’, then data is not compressible for the**
logical blocks indicated. If this bit is cleared to ‘0’, then no information on compression is
provided.

**Sequential Request (SEQREQ): If this bit is set to ‘1’, then this command is part of a**
sequential read that includes multiple Read commands. If this bit is cleared to ‘0’, then no
information on sequential access is provided.

05:04

**Access Latency (AL): This field specifies the expected access latency.**

**Value**

**Definition**
00b
None. No latency information provided.
01b
Idle. Longer latency acceptable.
10b
Normal. Typical latency.
11b
Low. Smallest possible latency.

03:00

**Access Frequency (AF): This field specifies the expected access frequency.**

**Value**

**Definition**
0h
No frequency information provided.
1h
Typical number of reads and writes expected for this LBA range.
2h
Infrequent writes and infrequent reads to the LBA range indicated.
3h
Infrequent writes and frequent reads to the LBA range indicated.
4h
Frequent writes and infrequent reads to the LBA range indicated.
5h
Frequent writes and frequent reads to the LBA range indicated.
6h
One time read. E.g., command is due to virus scan, backup, file copy, or
archive.
7h
Speculative read. The command is part of a prefetch operation.
8h
The LBA range is going to be overwritten in the near future.
9h to Fh
Reserved

**Figure 55: Read - Command Dword 13 if CETYPE is non-zero**

**Bits**

**Description**
31:16
Reserved
15:00

**Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE**
field. Refer to the Key Per I/O section in the NVM Express Base Specification.

**Figure 56: Read – Command Dword 14**

**Bits**

**Description**

31:00

**Expected Logical Block Tags Lower (ELBTL): This field and bits 47:00 of Command Dword 2 and**
Dword 3 specify the variable sized Expected Logical Block Storage Tag (ELBST) and Expected Initial
Logical Block Reference Tag (EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace
is not formatted to use end-to-end protection information, then this field is ignored by the controller.

**Figure 57: Read – Command Dword 15**

**Bits**

**Description**

31:16

**Expected Logical Block Application Tag Mask (ELBATM): This field specifies the Application Tag**
Mask expected value. If the namespace is not formatted to use end-to-end protection information, then
this field is ignored by the controller. Refer to section 5.3.


||Bits|||Description||
|---|---|---|---|---|---|
|07:00|||Dataset Management (DSM): This field indicates attributes for the LBA(s) being read.<br>Bits Description<br>Incompressible (INCPRS): If this bit is set to ‘1’, then data is not compressible for the<br>07 logical blocks indicated. If this bit is cleared to ‘0’, then no information on compression is<br>provided.<br>Sequential Request (SEQREQ): If this bit is set to ‘1’, then this command is part of a<br>06 sequential read that includes multiple Read commands. If this bit is cleared to ‘0’, then no<br>information on sequential access is provided.<br>Access Latency (AL): This field specifies the expected access latency.<br>Value Definition<br>05:04 00b None. No latency information provided.<br>01b Idle. Longer latency acceptable.<br>10b Normal. Typical latency.<br>11b Low. Smallest possible latency.<br>Access Frequency (AF): This field specifies the expected access frequency.<br>Value Definition<br>0h No frequency information provided.<br>1h Typical number of reads and writes expected for this LBA range.<br>2h Infrequent writes and infrequent reads to the LBA range indicated.<br>3h Infrequent writes and frequent reads to the LBA range indicated.<br>03:00 4h Frequent writes and infrequent reads to the LBA range indicated.<br>5h Frequent writes and frequent reads to the LBA range indicated.<br>One time read. E.g., command is due to virus scan, backup, file copy, or<br>6h<br>archive.<br>7h Speculative read. The command is part of a prefetch operation.<br>8h The LBA range is going to be overwritten in the near future.<br>9h to Fh Reserved|||


||Bits|||Description||
|---|---|---|---|---|---|
|07|||Incompressible (INCPRS): If this bit is set to ‘1’, then data is not compressible for the<br>logical blocks indicated. If this bit is cleared to ‘0’, then no information on compression is<br>provided.|||
|06|||Sequential Request (SEQREQ): If this bit is set to ‘1’, then this command is part of a<br>sequential read that includes multiple Read commands. If this bit is cleared to ‘0’, then no<br>information on sequential access is provided.|||
|05:04|||Access Latency (AL): This field specifies the expected access latency.<br>Value Definition<br>00b None. No latency information provided.<br>01b Idle. Longer latency acceptable.<br>10b Normal. Typical latency.<br>11b Low. Smallest possible latency.|||
|03:00|||Access Frequency (AF): This field specifies the expected access frequency.<br>Value Definition<br>0h No frequency information provided.<br>1h Typical number of reads and writes expected for this LBA range.<br>2h Infrequent writes and infrequent reads to the LBA range indicated.<br>3h Infrequent writes and frequent reads to the LBA range indicated.<br>4h Frequent writes and infrequent reads to the LBA range indicated.<br>5h Frequent writes and frequent reads to the LBA range indicated.<br>One time read. E.g., command is due to virus scan, backup, file copy, or<br>6h<br>archive.<br>7h Speculative read. The command is part of a prefetch operation.<br>8h The LBA range is going to be overwritten in the near future.<br>9h to Fh Reserved|||


||Value|||Definition||
|---|---|---|---|---|---|
|00b|||None. No latency information provided.|||
|01b|||Idle. Longer latency acceptable.|||
|10b|||Normal. Typical latency.|||
|11b|||Low. Smallest possible latency.|||


||Value|||Definition||
|---|---|---|---|---|---|
|0h|||No frequency information provided.|||
|1h|||Typical number of reads and writes expected for this LBA range.|||
|2h|||Infrequent writes and infrequent reads to the LBA range indicated.|||
|3h|||Infrequent writes and frequent reads to the LBA range indicated.|||
|4h|||Frequent writes and infrequent reads to the LBA range indicated.|||
|5h|||Frequent writes and frequent reads to the LBA range indicated.|||
|6h|||One time read. E.g., command is due to virus scan, backup, file copy, or<br>archive.|||
|7h|||Speculative read. The command is part of a prefetch operation.|||
|8h|||The LBA range is going to be overwritten in the near future.|||
|9h to Fh|||Reserved|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Reserved|||
|15:00|||Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE<br>field. Refer to the Key Per I/O section in the NVM Express Base Specification.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:00|||Expected Logical Block Tags Lower (ELBTL): This field and bits 47:00 of Command Dword 2 and<br>Dword 3 specify the variable sized Expected Logical Block Storage Tag (ELBST) and Expected Initial<br>Logical Block Reference Tag (EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace<br>is not formatted to use end-to-end protection information, then this field is ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Expected Logical Block Application Tag Mask (ELBATM): This field specifies the Application Tag<br>Mask expected value. If the namespace is not formatted to use end-to-end protection information, then<br>this field is ignored by the controller. Refer to section 5.3.|||

52

**Figure 57: Read – Command Dword 15**

**Bits**

**Description**

15:00

**Expected Logical Block Application Tag (ELBAT): This field specifies the Application Tag expected**
value. If the namespace is not formatted to use end-to-end protection information, then this field is
ignored by the controller. Refer to section 5.3.

**3.3.4.1**

**Command Completion**
When the command is completed with success or failure, the controller shall post a completion queue entry
to the associated I/O Completion Queue indicating the status for the command.
Read command specific status values are defined in Figure 58.

**Figure 58: Read – Command Specific Status Values**

**Value**

**Description**
80h

**Conflicting Attributes: The attributes specified in the command are conflicting.**

81h

**Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 53)**
settings specified in the command are invalid for the Protection Information with which the
namespace was formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the

**EILBRT field is invalid (refer to section 5.3.3).**

**Verify command**
The Verify command verifies integrity of stored information by reading data and metadata, if applicable, for
the LBAs indicated without transferring any data or metadata to the host. A Verify operation consists of the
controller actions (e.g., reading) that verify integrity of stored information during execution of a Verify
command. The command may specify protection information to be checked as part of the Verify operation.
Verify operations may be implemented via integrity checks of stored data and metadata. Metadata integrity
checks shall include protection information if the Verify command specifies checking of protection
information and the namespace is formatted with protection information.
If reading the data and metadata, if applicable, would result in an error being returned, then an error shall
be returned as a result of the Verify operation on that data and metadata, if applicable. In this situation, the
error that results from integrity checks may differ from the error that would result from reading (e.g., there
is no requirement that the Verify and Read commands return the same error). Setting the Limited Retry
(LR) bit to ‘1’ shall have the same effect in both the Read and Verify commands.
All data that is read or has its integrity checked by a Verify operation shall be included in the value of the
Data Units Read field in the SMART/Health Information log page, refer to the SMART / Health Information
section in the NVM Express Base Specification.
If the Verify Size Limit (VSL) field in the Identify Controller data structure is set to a non-zero value and:
a) if the Verify Support (NVMVFYS) bit in the Optional NVM Command Support field in the Identify
Controller data structure is set to ‘1’, then the VSL field indicates the recommended maximum data
size for the Verify command and any Verify command that specifies a logical block range whose
data size exceeds that recommended maximum may encounter delays in processing; and
b) if the NVMVFYS bit is cleared to ‘0’, then the VSL field indicates the data size limit for the Verify
command, and the controller shall abort any Verify command that specifies a logical block range
whose data size exceeds that limit with a status code of Invalid Field in Command.
The command uses Command Dword 2, Command Dword 3, Command Dword 10, Command Dword 11,
Command Dword 12, Command Dword 13, Command Dword 14, and Command Dword 15 fields.


||Bits|||Description||
|---|---|---|---|---|---|
|15:00|||Expected Logical Block Application Tag (ELBAT): This field specifies the Application Tag expected<br>value. If the namespace is not formatted to use end-to-end protection information, then this field is<br>ignored by the controller. Refer to section 5.3.|||


||Value|||Description||
|---|---|---|---|---|---|
|80h|||Conflicting Attributes: The attributes specified in the command are conflicting.|||
|81h|||Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 53)<br>settings specified in the command are invalid for the Protection Information with which the<br>namespace was formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the<br>EILBRT field is invalid (refer to section 5.3.3).|||

53

**Figure 59: Verify – Command Dword 2 and Dword 3**

**Bits**

**Description**
63:48
Reserved

47:00

**Expected Logical Block Tags Upper (ELBTU): This field and Command Dword 14 specify the variable**
sized Expected Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag
(EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-
end protection information, then this field is ignored by the controller.

**Figure 60: Verify – Command Dword 10 and Command Dword 11**

**Bits**

**Description**

63:00
Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block of data to be
verified as part of the operation. Command Dword 10 contains bits 31:00; Command Dword 11
contains bits 63:32.

**Figure 61: Verify – Command Dword 12**

**Bits**

**Description**
Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this
bit is cleared to ‘0’, then the controller should apply all available error recovery means before
completing the command with failure.
Force Unit Access (FUA): If this bit is set to ‘1’, then the controller shall flush any data and metadata
specified by the Verify command from any volatile cache before performing the Verify operation and
shall perform the Verify operation on data and metadata that have been committed to non-volatile
medium. There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has

**no effect.**

29:26

**Protection Information (PRINFO): Specifies the protection information action and check field, as**
defined in Figure 11. The Protection Information Check (PRCHK) field in the PRINFO field specifies
the protection information to be checked by the Verify operation. The Protection Information Action
(PRACT) bit in the PRINFO field is cleared to ‘0’ by the host. If the PRACT bit is not cleared to ’0’,

**then the controller shall abort the command with a status of Invalid Field in Command.**
Reserved
Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of Verify
operation as defined in Figure 12.
23:20
Reserved
19:16

**Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the**
command (refer to the Key Per I/O section in the NVM Express Base Specification).
15:00

**Number of Logical Blocks (NLB): This field indicates the number of logical blocks to be verified.**
This is a 0’s based value.

The definition of Command Dword 13 is based on the CETYPE value. If the CETYPE value is cleared to
0h, then Command Dword 13 is reserved. If the CETYPE value is non-zero, then Command Dword 13 is
defined in Figure 62.

**Figure 62: Verify - Command Dword 13 if CETYPE is non-zero**

**Bits**

**Description**
31:16
Reserved
15:00

**Command Extention Value (CEV): The definition of this field is dependent on the value of the CETYPE**
field. Refer to the Key Per I/O section in the NVM Express Base Specification.


||Bits|||Description||
|---|---|---|---|---|---|
|63:48|||Reserved|||
|47:00|||Expected Logical Block Tags Upper (ELBTU): This field and Command Dword 14 specify the variable<br>sized Expected Logical Block Storage Tag (ELBST) and Expected Initial Logical Block Reference Tag<br>(EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-<br>end protection information, then this field is ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:00|||Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block of data to be<br>verified as part of the operation. Command Dword 10 contains bits 31:00; Command Dword 11<br>contains bits 63:32.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31|||Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this<br>bit is cleared to ‘0’, then the controller should apply all available error recovery means before<br>completing the command with failure.|||
|30|||Force Unit Access (FUA): If this bit is set to ‘1’, then the controller shall flush any data and metadata<br>specified by the Verify command from any volatile cache before performing the Verify operation and<br>shall perform the Verify operation on data and metadata that have been committed to non-volatile<br>medium. There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has<br>no effect.|||
|29:26|||Protection Information (PRINFO): Specifies the protection information action and check field, as<br>defined in Figure 11. The Protection Information Check (PRCHK) field in the PRINFO field specifies<br>the protection information to be checked by the Verify operation. The Protection Information Action<br>(PRACT) bit in the PRINFO field is cleared to ‘0’ by the host. If the PRACT bit is not cleared to ’0’,<br>then the controller shall abort the command with a status of Invalid Field in Command.|||
|25|||Reserved|||
|24|||Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of Verify<br>operation as defined in Figure 12.|||
|23:20|||Reserved|||
|19:16|||Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the<br>command (refer to the Key Per I/O section in the NVM Express Base Specification).|||
|15:00|||Number of Logical Blocks (NLB): This field indicates the number of logical blocks to be verified.<br>This is a 0’s based value.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Reserved|||
|15:00|||Command Extention Value (CEV): The definition of this field is dependent on the value of the CETYPE<br>field. Refer to the Key Per I/O section in the NVM Express Base Specification.|||

54

**Figure 63: Verify – Command Dword 14**

**Bits**

**Description**

31:00

**Expected Logical Block Tags Lower (ELBTL): This field and bits 47:00 of Command Dword 2 and**
Dword 3 specify the variable sized Expected Logical Block Storage Tag (ELBST) and Expected Initial
Logical Block Reference Tag (EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace
is not formatted to use end-to-end protection information, then this field is ignored by the controller.

**Figure 64: Verify – Command Dword 15**

**Bits**

**Description**

31:16

**Expected Logical Block Application Tag Mask (ELBATM): This field specifies the Application Tag**
Mask expected value. If the namespace is not formatted to use end-to-end protection information,
then this field is ignored by the controller. Refer to section 5.3.

15:00

**Expected Logical Block Application Tag (ELBAT): This field specifies the Application Tag expected**
value. If the namespace is not formatted to use end-to-end protection information, then this field is

**ignored by the controller. Refer to section 5.3.**

**3.3.5.1**

**Command Completion**
Upon completion of the Verify command, the controller posts a completion queue entry (CQE) to the
associated I/O Completion Queue. The status code types and values that may be used in a CQE for the
Verify command include the status code type and status code values for all Media and Data Integrity Errors
for the NVM Command Set that are applicable to the Read command (e.g., Unrecovered Read Error). For
more information of status codes for the NVM Command Set refer to section 3.1.
Verify command specific status values are defined in Figure 65.

**Figure 65: Verify – Command Specific Status Values**

**Value**

**Description**

81h

**Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 61)**
settings specified in the command are invalid for the Protection Information with which the namespace
was formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the EILBRT field
is invalid (refer to section 5.3.3).

**Write command**
The Write command writes data and metadata, if applicable, to the I/O controller for the logical blocks
indicated. The host may also specify protection information to include as part of the operation.
The command uses Command Dword 2, Command Dword 3, Command Dword 10, Command Dword 11,
Command Dword 12, Command Dword 13, Command Dword 14, and Command Dword 15 fields. If the
command uses PRPs for the data transfer, then the Metadata Pointer, PRP Entry 1, and PRP Entry 2 fields
are used. If the command uses SGLs for the data transfer, then the Metadata SGL Segment Pointer and
SGL Entry 1 fields are used.

**Figure 66: Write – Metadata Pointer**

**Bits**

**Description**
63:00
Metadata Pointer (MPTR): This field contains the Metadata Pointer, if applicable. Refer to the Common
Command Format figure in the NVM Express Base Specification for the definition of this field.


||Bits|||Description||
|---|---|---|---|---|---|
|31:00|||Expected Logical Block Tags Lower (ELBTL): This field and bits 47:00 of Command Dword 2 and<br>Dword 3 specify the variable sized Expected Logical Block Storage Tag (ELBST) and Expected Initial<br>Logical Block Reference Tag (EILBRT) fields, which are defined in section 5.3.1.4.1. If the namespace<br>is not formatted to use end-to-end protection information, then this field is ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Expected Logical Block Application Tag Mask (ELBATM): This field specifies the Application Tag<br>Mask expected value. If the namespace is not formatted to use end-to-end protection information,<br>then this field is ignored by the controller. Refer to section 5.3.|||
|15:00|||Expected Logical Block Application Tag (ELBAT): This field specifies the Application Tag expected<br>value. If the namespace is not formatted to use end-to-end protection information, then this field is<br>ignored by the controller. Refer to section 5.3.|||


||Value|||Description||
|---|---|---|---|---|---|
|81h|||Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 61)<br>settings specified in the command are invalid for the Protection Information with which the namespace<br>was formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the EILBRT field<br>is invalid (refer to section 5.3.3).|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:00|||Metadata Pointer (MPTR): This field contains the Metadata Pointer, if applicable. Refer to the Common<br>Command Format figure in the NVM Express Base Specification for the definition of this field.|||

55

**Figure 67: Write – Data Pointer**

**Bits**

**Description**

127:00
Data Pointer (DPTR): This field specifies the location of a data buffer where data is transferred from.
Refer to the Common Command Format figure in the NVM Express Base Specification for the definition
of this field.

**Figure 68: Write – Command Dword 2 and Dword 3**

**Bits**

**Description**
63:48
Reserved

47:00

**Logical Block Tags Upper (LBTU): This field and Command Dword 14 specify the variable sized**
Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT) fields, which are
defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-end protection information,
then this field is ignored by the controller.

**Figure 69: Write – Command Dword 10 and Command Dword 11**

**Bits**

**Description**
63:00
Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block to be written as part
of the operation. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits 63:32.

**Figure 70: Write – Command Dword 12**

**Bits**

**Description**
Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this bit
is cleared to ‘0’, then the controller should apply all available error recovery means to write the data to
the NVM.
Force Unit Access (FUA): If this bit is set to ‘1’, then for data and metadata, if any, associated with
logical blocks specified by the Write command, the controller shall write that data and metadata, if any,
to non-volatile medium before indicating command completion.
There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has no effect.
29:26

**Protection Information (PRINFO): Specifies the protection information action and check field, as**

**defined in Figure 11.**
Reserved
Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of end-to-
end data protection processing as defined in Figure 12.
23:20
Directive Type (DTYPE): Specifies the Directive Type associated with the Directive Specific field (refer
to the Directives section in the NVM Express Base Specification).
19:16

**Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the**
command (refer to the Key Per I/O section in the NVM Express Base Specification).

**15:00**
Number of Logical Blocks (NLB): This field indicates the number of logical blocks to be written. This is

**a 0’s based value.**

The definition of Command Dword 13 is based on the CETYPE value. If the CETYPE value is cleared to
0h, then Command Dword 13 is defined in Figure 71. If the CETYPE value is non-zero, then Command
Dword 13 is defined in Figure 72.

**Figure 71: Write – Command Dword 13 if CETYPE is cleared to 0h**

**Bits**

**Description**
31:16
Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type
field (refer to the Directives section in the NVM Express Base Specification).


||Bits|||Description||
|---|---|---|---|---|---|
|127:00|||Data Pointer (DPTR): This field specifies the location of a data buffer where data is transferred from.<br>Refer to the Common Command Format figure in the NVM Express Base Specification for the definition<br>of this field.|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:48|||Reserved|||
|47:00|||Logical Block Tags Upper (LBTU): This field and Command Dword 14 specify the variable sized<br>Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT) fields, which are<br>defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-end protection information,<br>then this field is ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|63:00|||Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block to be written as part<br>of the operation. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits 63:32.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31|||Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this bit<br>is cleared to ‘0’, then the controller should apply all available error recovery means to write the data to<br>the NVM.|||
|30|||Force Unit Access (FUA): If this bit is set to ‘1’, then for data and metadata, if any, associated with<br>logical blocks specified by the Write command, the controller shall write that data and metadata, if any,<br>to non-volatile medium before indicating command completion.<br>There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has no effect.|||
|29:26|||Protection Information (PRINFO): Specifies the protection information action and check field, as<br>defined in Figure 11.|||
|25|||Reserved|||
|24|||Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of end-to-<br>end data protection processing as defined in Figure 12.|||
|23:20|||Directive Type (DTYPE): Specifies the Directive Type associated with the Directive Specific field (refer<br>to the Directives section in the NVM Express Base Specification).|||
|19:16|||Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the<br>command (refer to the Key Per I/O section in the NVM Express Base Specification).|||
|15:00|||Number of Logical Blocks (NLB): This field indicates the number of logical blocks to be written. This is<br>a 0’s based value.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type<br>field (refer to the Directives section in the NVM Express Base Specification).|||

56

**Figure 71: Write – Command Dword 13 if CETYPE is cleared to 0h**

**Bits**

**Description**
15:08
Reserved

07:00

**Dataset Management (DSM): This field indicates attributes for the LBA(s) being written.**

**Bits**

**Definition**

**Incompressible (INCPRS): If this bit is set to ‘1’, then data is not compressible for the logical**
blocks indicated. If this bit is cleared to ‘0’, then no information on compression is provided.

**Sequential Request (SEQREQ): If this bit is set to ‘1’, then this command is part of a**
sequential write that includes multiple Write commands. If this bit is cleared to ‘0’, then no
information on sequential access is provided.

05:04

**Access Latency (AL): This field specifies the exected access latency.**

**Value**

**Definition**
00b
None. No latency information provided.
01b
Idle. Longer latency acceptable.
10b
Normal. Typical latency.
11b
Low. Smallest possible latency.

03:00

**Access Frequency (AF): This field specifies the expected access frequency.**

**Value**

**Definition**
0h
No frequency information provided.
1h
Typical number of reads and writes expected for this LBA range.
2h
Infrequent writes and infrequent reads to the LBA range indicated.
3h
Infrequent writes and frequent reads to the LBA range indicated.
4h
Frequent writes and infrequent reads to the LBA range indicated.
5h
Frequent writes and frequent reads to the LBA range indicated.
6h
One time write. E.g., command is due to virus scan, backup, file copy, or
archive.
7h to Fh
Reserved

**Figure 72: Write - Command Dword 13 if CETYPE is non-zero**

**Bits**

**Description**
31:16
Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type
field (refer to the Key Per I/O section in the NVM Express Base Specification).
15:00

**Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE**
field. Refer to the Key Per I/O section in the NVM Express Base Specification.

**Figure 73: Write – Command Dword 14**

**Bits**

**Description**

31:00

**Logical Block Tags Lower (LBTL): This field and bits 47:00 of Command Dword 2 and Dword 3 specify**
the variable sized Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT)
fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-end
protection information, then this field is ignored by the controller.

**Figure 74: Write – Command Dword 15**

**Bits**

**Description**

31:16

**Logical Block Application Tag Mask (LBATM): This field specifies the Application Tag Mask value. If**
the namespace is not formatted to use end-to-end protection information, then this field is ignored by the
controller. Refer to section 5.3.

15:00
Logical Block Application Tag (LBAT): This field specifies the Application Tag value. If the namespace
is not formatted to use end-to-end protection information, then this field is ignored by the controller. Refer
to section 5.3.


||Bits|||Description||
|---|---|---|---|---|---|
|15:08|||Reserved|||
|07:00|||Dataset Management (DSM): This field indicates attributes for the LBA(s) being written.<br>Bits Definition<br>Incompressible (INCPRS): If this bit is set to ‘1’, then data is not compressible for the logical<br>07<br>blocks indicated. If this bit is cleared to ‘0’, then no information on compression is provided.<br>Sequential Request (SEQREQ): If this bit is set to ‘1’, then this command is part of a<br>06 sequential write that includes multiple Write commands. If this bit is cleared to ‘0’, then no<br>information on sequential access is provided.<br>Access Latency (AL): This field specifies the exected access latency.<br>Value Definition<br>05:04 00b None. No latency information provided.<br>01b Idle. Longer latency acceptable.<br>10b Normal. Typical latency.<br>11b Low. Smallest possible latency.<br>Access Frequency (AF): This field specifies the expected access frequency.<br>Value Definition<br>0h No frequency information provided.<br>1h Typical number of reads and writes expected for this LBA range.<br>2h Infrequent writes and infrequent reads to the LBA range indicated.<br>03:00 3h Infrequent writes and frequent reads to the LBA range indicated.<br>4h Frequent writes and infrequent reads to the LBA range indicated.<br>5h Frequent writes and frequent reads to the LBA range indicated.<br>One time write. E.g., command is due to virus scan, backup, file copy, or<br>6h<br>archive.<br>7h to Fh Reserved|||


||Bits|||Definition||
|---|---|---|---|---|---|
|07|||Incompressible (INCPRS): If this bit is set to ‘1’, then data is not compressible for the logical<br>blocks indicated. If this bit is cleared to ‘0’, then no information on compression is provided.|||
|06|||Sequential Request (SEQREQ): If this bit is set to ‘1’, then this command is part of a<br>sequential write that includes multiple Write commands. If this bit is cleared to ‘0’, then no<br>information on sequential access is provided.|||
|05:04|||Access Latency (AL): This field specifies the exected access latency.<br>Value Definition<br>00b None. No latency information provided.<br>01b Idle. Longer latency acceptable.<br>10b Normal. Typical latency.<br>11b Low. Smallest possible latency.|||
|03:00|||Access Frequency (AF): This field specifies the expected access frequency.<br>Value Definition<br>0h No frequency information provided.<br>1h Typical number of reads and writes expected for this LBA range.<br>2h Infrequent writes and infrequent reads to the LBA range indicated.<br>3h Infrequent writes and frequent reads to the LBA range indicated.<br>4h Frequent writes and infrequent reads to the LBA range indicated.<br>5h Frequent writes and frequent reads to the LBA range indicated.<br>One time write. E.g., command is due to virus scan, backup, file copy, or<br>6h<br>archive.<br>7h to Fh Reserved|||


||Value|||Definition||
|---|---|---|---|---|---|
|00b|||None. No latency information provided.|||
|01b|||Idle. Longer latency acceptable.|||
|10b|||Normal. Typical latency.|||
|11b|||Low. Smallest possible latency.|||


||Value|||Definition||
|---|---|---|---|---|---|
|0h|||No frequency information provided.|||
|1h|||Typical number of reads and writes expected for this LBA range.|||
|2h|||Infrequent writes and infrequent reads to the LBA range indicated.|||
|3h|||Infrequent writes and frequent reads to the LBA range indicated.|||
|4h|||Frequent writes and infrequent reads to the LBA range indicated.|||
|5h|||Frequent writes and frequent reads to the LBA range indicated.|||
|6h|||One time write. E.g., command is due to virus scan, backup, file copy, or<br>archive.|||
|7h to Fh|||Reserved|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type<br>field (refer to the Key Per I/O section in the NVM Express Base Specification).|||
|15:00|||Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE<br>field. Refer to the Key Per I/O section in the NVM Express Base Specification.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:00|||Logical Block Tags Lower (LBTL): This field and bits 47:00 of Command Dword 2 and Dword 3 specify<br>the variable sized Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT)<br>fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-end<br>protection information, then this field is ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Logical Block Application Tag Mask (LBATM): This field specifies the Application Tag Mask value. If<br>the namespace is not formatted to use end-to-end protection information, then this field is ignored by the<br>controller. Refer to section 5.3.|||
|15:00|||Logical Block Application Tag (LBAT): This field specifies the Application Tag value. If the namespace<br>is not formatted to use end-to-end protection information, then this field is ignored by the controller. Refer<br>to section 5.3.|||

57

**3.3.6.1**

**Command Completion**
When the command is completed with success or failure, the controller shall post a completion queue entry
to the associated I/O Completion Queue indicating the status for the command.
Write command specific errors (i.e., SCT fields set to 1h) are shown in Figure 75.

**Figure 75: Write – Command Specific Status Values**

**Value**

**Definition**
80h

**Conflicting Attributes: The attributes specified in the command are conflicting.**

81h
Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 70) settings
specified in the command are invalid for the Protection Information with which the namespace was
formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the ILBRT field is invalid

**(refer to section 5.3.3).**

82h
Attempted Write to Read Only Range: The LBA range specified contains read-only blocks. The controller
shall not return this status value if the read-only condition on the media is a result of a change in the write
protection state of a namespace (refer to the Namespace Write Protection section in the NVM Express

**Base Specification).**

**Write Uncorrectable command**
The Write Uncorrectable command is used to mark a range of logical blocks as invalid. When the specified
logical block(s) are read after this operation, a failure is returned with Unrecovered Read Error status. To
clear the invalid logical block status, a write operation is performed on those logical blocks.
If the Write Uncorrectable Size Limit (WUSL) field in the Identify Controller data structure is set to a non-
zero value and:
a) if the Write Uncorrectable Support Variants (NVMWUSV) bit is set to ‘1’ in the Optional NVM
Command Support field in the Identify Controller data structure, then the WUSL field indicates the
recommended maximum data size for the Write Uncorrectable command and any Write
Uncorrectable command that specifies a logical block range whose data size exceeds that
recommended maximum may encounter delays in processing; and
b) if the NVMWUSV bit is cleared to ‘0’, then the WUSL field indicates the data size limit for the Write
Uncorrectable command, and the controller shall abort any Write Uncorrectable command that
specifies a logical block range whose data size exceeds that limit with a status of Invalid Field in
Command.
The fields used are Command Dword 10, Command Dword 11, and Command Dword 12 fields. All other
command specific fields are reserved.

**Figure 76: Write Uncorrectable – Command Dword 10 and Command Dword 11**

**Bits**

**Description**

63:00

**Starting LBA (SLBA): This field specifies the 64-bit address of the first logical block to become**
uncorrectable as part of the operation. Command Dword 10 contains bits 31:00; Command Dword 11
contains bits 63: 32.

**Figure 77: Write Uncorrectable – Command Dword 12**

**Bits**

**Description**
31:24
Reserved
23:20
Directive Type (DTYPE): Specifies the Directive Type associated with the Directive Specific field (refer
to the Directives section in the NVM Express Base Specification).
19:16
Reserved


||Value||Definition||
|---|---|---|---|---|
|80h||Conflicting Attributes: The attributes specified in the command are conflicting.|||
|81h||Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 70) settings<br>specified in the command are invalid for the Protection Information with which the namespace was<br>formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the ILBRT field is invalid<br>(refer to section 5.3.3).|||
|82h||Attempted Write to Read Only Range: The LBA range specified contains read-only blocks. The controller<br>shall not return this status value if the read-only condition on the media is a result of a change in the write<br>protection state of a namespace (refer to the Namespace Write Protection section in the NVM Express<br>Base Specification).|||


||Bits||Description||
|---|---|---|---|---|
|63:00|||Starting LBA (SLBA): This field specifies the 64-bit address of the first logical block to become<br>uncorrectable as part of the operation. Command Dword 10 contains bits 31:00; Command Dword 11<br>contains bits 63: 32.||


||Bits||Description||
|---|---|---|---|---|
|31:24|||Reserved||
|23:20|||Directive Type (DTYPE): Specifies the Directive Type associated with the Directive Specific field (refer<br>to the Directives section in the NVM Express Base Specification).||
|19:16|||Reserved||

58

**Figure 77: Write Uncorrectable – Command Dword 12**

**Bits**

**Description**

**15:00**

**Number of Logical Blocks (NLB): This field specifies the number of logical blocks to become**

**uncorrectable. This is a 0’s based value.**

**Figure 78: Write Uncorrectable – Command Dword 13**

**Bits**

**Description**
31:16
Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type
field (refer to the Directives section in the NVM Express Base Specification).

**15:00**

**Reserved**

**3.3.7.1**

**Command Completion**
Upon command completion, the controller shall post a completion queue entry to the associated I/O
Completion Queue indicating the status for the command.
Write Uncorrectable command specific errors (i.e., SCT field set to 1h) are shown in Figure 79.

**Figure 79: Write Uncorrectable – Command Specific Status Values**

**Value**

**Description**

82h

**Attempted Write to Read Only Range: The LBA range specified contains read-only blocks. The**
controller shall not return this status value if the read-only condition on the media is a result of a change
in the write protection state of a namespace (refer to the Namespace Write Protection section in the NVM
Express Base Specification).

**Write Zeroes command**
The Write Zeroes command is used to clear a range of logical blocks or all of the logical blocks in an entire
namespace to zero. Non-PI related metadata for this command, if any, shall be all bytes cleared to 0h. The
protection information for logical blocks written to the media is updated based on CDW12.PRINFO. If the
Protection Information Action (PRACT) bit is cleared to ‘0’, then the protection information for this command
shall be all zeroes. If the PRACT bit is set to ‘1’, then the protection information shall be based on the End-
to-end Data Protection Type Settings (DPS) field in the Identify Namespace data structure (refer to Figure
114), CDW15.LBATM, CDW15.LBAT, as well as CDW2/3 and CDW14 content as described in section
5.3.1.4.1. Protection information of all zeroes is generated if the PRACT bit is cleared to 0h resulting in
invalid protection information; therefore, the host should set the PRACT bit to ‘1’ to generate valid protection
information.
After successful completion of a Write Zeroes command that specifies:
•
clearing a range of logical blocks to zero, the value returned by subsequent successful reads of
logical blocks and associated metadata (excluding protection information) in this range shall be all
bytes cleared to 0h until a write occurs to that range of logical blocks; or
•
clearing all of the logical blocks in an entire namespace to zero, the value returned by subsequent
reads of each logical block in that namespace shall be all bytes cleared to 0h until a write occurs
to that logical block.
For each logical block in the range specified by a Write Zeroes command, if the namespace supports
clearing all bytes to 0h in the values read (e.g., the Deallocation Read Behavior (DRB) field in the DLFEAT


||Bits|||Description||
|---|---|---|---|---|---|
|15:00|||Number of Logical Blocks (NLB): This field specifies the number of logical blocks to become<br>uncorrectable. This is a 0’s based value.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type<br>field (refer to the Directives section in the NVM Express Base Specification).|||
|15:00|||Reserved|||


||Value|||Description||
|---|---|---|---|---|---|
|82h|||Attempted Write to Read Only Range: The LBA range specified contains read-only blocks. The<br>controller shall not return this status value if the read-only condition on the media is a result of a change<br>in the write protection state of a namespace (refer to the Namespace Write Protection section in the NVM<br>Express Base Specification).|||

59
field is set to 001b) from a deallocated logical block and its metadata (excluding protection information),
and the value of the Deallocate bit (CDW12.DEAC) in that Write Zeroes command is:
•
set to ‘1’, then the controller should deallocate that logical block; and
•
cleared to ‘0’, then the controller may deallocate that logical block.
For each logical block in the range specified by a Write Zeroes command, if the namespace does not
support clearing all bytes to 0h in the values read from that logical block and its metadata (excluding the
protection information) when that logical block is deallocated, then the controller shall not deallocate that
logical block.
If a logical block in the range specified by a Write Zeroes command is deallocated as a result of that
command, then:
•
the DULBE bit in the Error Recovery feature (refer to section 4.1.3.2) affects whether subsequent
reads of that deallocated logical block are able to succeed (refer to section 3.3.3.2.1); and
•
the values of protection information, if any, returned by subsequent successful reads of that
deallocated logical block are specified in section 3.3.3.2.1.
If a logical block in the range specified by a Write Zeroes command is not deallocated as a result of that
command, then the values of protection information, if any, returned by subsequent successful reads of
that logical block shall be based on CDW12.PRINFO in that Write Zeroes command.
If the Write Zeroes Size Limit (WZSL) field in the I/O Command Set specific Identify Controller data structure
for the NVM Command Set (refer to Figure 120) is set to a non-zero value and the Write Zeroes with
Deallocate Size Limit (WZDSL) field in that data structure is cleared to 0h, then:

**a) if the Write Zeroes Support Variants (NVMWZSV) bit is set to ‘1’ in the Optional NVMe Command**
Support field in the Identify Controller data structure, then the WZSL field indicates the
recommended maximum data size for the Write Zeroes command and any Write Zeroes command
that specifies a logical block range whose data size exceeds that recommended maximum may
encounter delays in processing; and
b) if the NVMWZSV bit is cleared to ‘0’, then the WZSL field indicates the maximum data size limit for
the Write Zeroes command, and the controller shall abort any Write Zeroes command that specifies
a logical block range whose data size exceeds that limit with a status of Invalid Field in Command.
If the WZSL field is set to a non-zero value and the WZDSL field is set to a non-zero value, then:
a) if the NVMWZSV bit is set to ‘1’, then:
•
the WZDSL field indicates the recommended maximum data size for any Write Zeroes
command that has the Deallocate bit set to ‘1’;
•
the WZSL field indicates the recommended maximum data size for any Write Zeroes command
that has the Deallocate bit cleared to ‘0’; and
•
any Write Zeroes command that specifies a logical block range whose data size exceeds the
applicable recommended maximum may encounter delays in processing;
and
b) if the NVMWZSV bit is cleared to ‘0’, then:
•
the WZDSL field indicates the maximum data size limit for any Write Zeroes command that has
the Deallocate bit set to ‘1’;
•
the WZSL field indicates the maximum data size limit for any Write Zeroes command that has
the Deallocate bit cleared to ‘0’; and
60
•
the controller shall abort any Write Zeroes command that specifies a logical block range whose
data size exceeds the applicable data size limit with a status code of Invalid Field in Command.
The WZSL field and the WZDSL field do not apply to Write Zeroes commands that have the Namespace
Zeroes (NSZ) bit (refer to Figure 82) set to ‘1’.
The Namespace Zeroes (NSZ) bit is set to ‘1’ to request that the controller clear all of the logical blocks to
zero in the entire specified namespace by deallocating all logical blocks in that namespace. This
functionality is only supported when the Deallocate bit is also set to ‘1’ and the specified namespace
supports clearing all bytes to 0h in the values read from a deallocated logical block and its metadata
(excluding protection information) (e.g., as indicated by the DLFEAT field in Identify Namespace data
structure being set to 001b (refer to Figure 114)).
If the NSZ bit is set to ‘1’ in a Write Zeroes command and either:
•
the Deallocate bit is cleared to ‘0’; or
•
the specified namespace does not support clearing all bytes to 0h in the values read from a
deallocated logical block and its metadata (excluding protection information),
then the controller shall abort that command with a status code of Invalid Field in Command.
Controller support for the NSZ bit is indicated by setting the NSZS bit to ‘1’ in the ONCS field in the Identify
Controller data structure. If the controller supports the NSZ bit and the NSZ bit is set to ‘1’ in a Write Zeroes
command, then the controller ignores the Starting LBA (SLBA) field (refer to Figure 81) and the Number of
Logical Blocks (NLB) field (refer to Figure 82) in that command.
If the controller does not support the NSZ bit (i.e., the NSZS bit in the ONCS field in the Identify Controller
data structure is cleared to ‘0’), then the controller is not required to check whether the NSZ bit is cleared
to ‘0’; and may clear to zero the range of logical blocks specified by the SLBA field and NLB field instead
of clearing all of the logical blocks to zero in the entire namespace.
The host is able to determine whether or not the controller cleared all of the logical blocks to zero in the
entire specified namespace by checking the LBAs Cleared to Zero (LBACZ) bit of Dword 0 in the completion
queue entry (CQE) for the Write Zeroes command (refer to Figure 87). The controller sets that bit to ‘1’ if
all of the logical blocks have been cleared to zero in the entire specified namespace (refer to section
3.3.8.1). The host should check this bit for any Write Zeroes command in which the NSZ bit is set to ‘1’ to
determine whether or not the controller cleared all of the logical blocks to zero in the entire specified
namespace.
The fields used are Command Dword 2, Command Dword 3, Command Dword 10, Command Dword 11,
Command Dword 12, Command Dword 13, Command Dword 14, and Command Dword 15 fields.

**Figure 80: Write Zeroes – Command Dword 2 and Dword 3**

**Bits**

**Description**
63:48
Reserved

47:00

**Logical Block Tags Upper (LBTU): This field and Command Dword 14 specify the variable sized**
Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT) fields, which are
defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-end protection information,
then this field is ignored by the controller.


||Bits|||Description||
|---|---|---|---|---|---|
|63:48|||Reserved|||
|47:00|||Logical Block Tags Upper (LBTU): This field and Command Dword 14 specify the variable sized<br>Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT) fields, which are<br>defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-end protection information,<br>then this field is ignored by the controller.|||

61

**Figure 81: Write Zeroes – Command Dword 10 and Command Dword 11**

**Bits**

**Description**

63:00
Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block to be written as part
of the operation. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits 63:32.
If the NSZ bit (refer to Figure 82) is set to ‘1’ and NSZS bit is set to ‘1’ in the Optional NVMe Command
Support (ONCS) field in the Identify Controller data structure, then this field should be cleared to 0h by
the host and shall be ignored by the controller.

**Figure 82: Write Zeroes – Command Dword 12**

**Bits**

**Description**
Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this bit
is cleared to ‘0’, then the controller should apply all available error recovery means to write the data to
the NVM.
Force Unit Access (FUA): If this bit is set to ‘1’, then the controller shall write the data, and metadata,
if any, to non-volatile medium before indicating command completion.
There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has no effect.
29:26

**Protection Information (PRINFO): Specifies the protection information action and check field, as**

**defined in Figure 11. The Protection Information Check (PRCHK) field shall be cleared to 000b.**
Deallocate (DEAC): If this bit is set to ‘1’, then the host is requesting that the controller deallocate the
specified logical blocks. If this bit is cleared to ‘0’, then the host is not requesting that the controller
deallocate the specified logical blocks.
If the NSZ bit is set to ‘1’ and this bit is cleared to ‘0’, then the controller shall abort the command with a
status code of Invalid Field in Command.
Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of end-to-

**end data protection processing as defined in Figure 12. This bit shall be cleared to ‘0’.**
Namespace Zeroes (NSZ): If this bit is set to '1' and the Deallocate bit is set to ‘1’, then the Write Zeroes
command is requesting that the controller clear all logical blocks to zero in the entire namespace. If bit
NSZS in the Optional NVM Command Support (ONCS) field in the Identify Controller data structure is
cleared to ‘0’, then this bit has no effect.
22:20
Directive Type (DTYPE): Specifies the Directive Type associated with the Directive Specific field (refer
to the Directives section in the NVM Express Base Specification).
19:16

**Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the**
command (refer to the Key Per I/O section in the NVM Express Base Specification).

**15:00**
Number of Logical Blocks (NLB): This field indicates the number of logical blocks to be written. This is
a 0’s based value.
If the NSZ bit is set to ‘1’, then this field should be cleared to 0h by the host and shall be ignored by the
controller.

The definition of Command Dword 13 is based on the CETYPE value. If the CETYPE value is cleared to
0h, then Command Dword 13 is defined in Figure 83. If the CETYPE value is non-zero, then Command
Dword 13 is defined in Figure 84.

**Figure 83: Write Zeroes – Command Dword 13 if CETYPE is cleared to 0h**

**Bits**

**Description**
31:16
Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type
field (refer to the Directives section in the NVM Express Base Specification).
15:00
Reserved


||Bits|||Description||
|---|---|---|---|---|---|
|63:00|||Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block to be written as part<br>of the operation. Command Dword 10 contains bits 31:00; Command Dword 11 contains bits 63:32.<br>If the NSZ bit (refer to Figure 82) is set to ‘1’ and NSZS bit is set to ‘1’ in the Optional NVMe Command<br>Support (ONCS) field in the Identify Controller data structure, then this field should be cleared to 0h by<br>the host and shall be ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31|||Limited Retry (LR): If this bit is set to ‘1’, then the controller should apply limited retry efforts. If this bit<br>is cleared to ‘0’, then the controller should apply all available error recovery means to write the data to<br>the NVM.|||
|30|||Force Unit Access (FUA): If this bit is set to ‘1’, then the controller shall write the data, and metadata,<br>if any, to non-volatile medium before indicating command completion.<br>There is no implied ordering with other commands. If this bit is cleared to ‘0’, then this bit has no effect.|||
|29:26|||Protection Information (PRINFO): Specifies the protection information action and check field, as<br>defined in Figure 11. The Protection Information Check (PRCHK) field shall be cleared to 000b.|||
|25|||Deallocate (DEAC): If this bit is set to ‘1’, then the host is requesting that the controller deallocate the<br>specified logical blocks. If this bit is cleared to ‘0’, then the host is not requesting that the controller<br>deallocate the specified logical blocks.<br>If the NSZ bit is set to ‘1’ and this bit is cleared to ‘0’, then the controller shall abort the command with a<br>status code of Invalid Field in Command.|||
|24|||Storage Tag Check (STC): This bit specifies the Storage Tag field shall be checked as part of end-to-<br>end data protection processing as defined in Figure 12. This bit shall be cleared to ‘0’.|||
|23|||Namespace Zeroes (NSZ): If this bit is set to '1' and the Deallocate bit is set to ‘1’, then the Write Zeroes<br>command is requesting that the controller clear all logical blocks to zero in the entire namespace. If bit<br>NSZS in the Optional NVM Command Support (ONCS) field in the Identify Controller data structure is<br>cleared to ‘0’, then this bit has no effect.|||
|22:20|||Directive Type (DTYPE): Specifies the Directive Type associated with the Directive Specific field (refer<br>to the Directives section in the NVM Express Base Specification).|||
|19:16|||Command Extension Type (CETYPE): Specifies the Command Extension Type that applies to the<br>command (refer to the Key Per I/O section in the NVM Express Base Specification).|||
|15:00|||Number of Logical Blocks (NLB): This field indicates the number of logical blocks to be written. This is<br>a 0’s based value.<br>If the NSZ bit is set to ‘1’, then this field should be cleared to 0h by the host and shall be ignored by the<br>controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type<br>field (refer to the Directives section in the NVM Express Base Specification).|||
|15:00|||Reserved|||

62

**Figure 84: Write Zeroes – Command Dword 13 if CETYPE is non-zero**

**Bits**

**Description**
31:16
Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type
field (refer to the Directives section in the NVM Express Base Specification).
15:00

**Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE**
field. Refer to the Key Per I/O section in the NVM Express Base Specification.

**Figure 85: Write Zeroes – Command Dword 14**

**Bits**

**Description**

31:00

**Logical Block Tags Lower (LBTL): This field and bits 47:00 of Command Dword 2 and Dword 3 specify**
the variable sized Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT)
fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-end
protection information, then this field is ignored by the controller.

**Figure 86: Write Zeroes – Command Dword 15**

**Bits**

**Description**

31:16

**Logical Block Application Tag Mask (LBATM): This field indicates the Application Tag Mask value. If**
the namespace is not formatted to use end-to-end protection information, then this field is ignored by the
controller. Refer to section 5.3.

15:00
Logical Block Application Tag (LBAT): This field indicates the Application Tag value. If the namespace
is not formatted to use end-to-end protection information, then this field is ignored by the controller. Refer
to section 5.3.

**3.3.8.1**

**Command Completion**
Upon completion of the Write Zeroes command, the controller shall post a completion queue entry to the
associated I/O Completion Queue indicating the status for the command.
If the command does not complete successfully (i.e., completes with a status code other than Successful
Completion), then the controller may or may not have completed the requested clearing of logical blocks to
zero.
If the command has the Namespace Zeroes (NSZ) bit cleared to ‘0’ and completes successfully, then the
logical blocks specified by the command have been cleared to zero. If the command has the Namespace
Zeroes (NSZ) bit set to ‘1’ and completes successfully, then the LBAs Cleared to Zero bit in completion
queue entry Dword 0 indicates whether the specified logical blocks have been cleared to zero as defined
in Figure 87.

**Figure 87: Write Zeroes – Completion Queue Entry Dword 0**

**Bits**

**Description**
31:01
Reserved

**LBAs Cleared to Zero (LBACZ): If the command has the Namespace Zeroes (NSZ) bit set to ‘1’ and**
completes successfully, then this bit is defined as follows:

**Value**

**Definition**
0b
The number of logical blocks specified by the Number of Logical Blocks (NLB) field have
been cleared to zero.
1b
All logical blocks in the entire namespace have been cleared to zero.

Write Zeroes command specific status values (i.e., SCT field set to 1h) are shown in Figure 88.


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Directive Specific (DSPEC): Specifies the Directive Specific value associated with the Directive Type<br>field (refer to the Directives section in the NVM Express Base Specification).|||
|15:00|||Command Extension Value (CEV): The definition of this field is dependent on the value of the CETYPE<br>field. Refer to the Key Per I/O section in the NVM Express Base Specification.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:00|||Logical Block Tags Lower (LBTL): This field and bits 47:00 of Command Dword 2 and Dword 3 specify<br>the variable sized Logical Block Storage Tag (LBST) and Initial Logical Block Reference Tag (ILBRT)<br>fields, which are defined in section 5.3.1.4.1. If the namespace is not formatted to use end-to-end<br>protection information, then this field is ignored by the controller.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:16|||Logical Block Application Tag Mask (LBATM): This field indicates the Application Tag Mask value. If<br>the namespace is not formatted to use end-to-end protection information, then this field is ignored by the<br>controller. Refer to section 5.3.|||
|15:00|||Logical Block Application Tag (LBAT): This field indicates the Application Tag value. If the namespace<br>is not formatted to use end-to-end protection information, then this field is ignored by the controller. Refer<br>to section 5.3.|||


||Bits|||Description||
|---|---|---|---|---|---|
|31:01|||Reserved|||
|00|||LBAs Cleared to Zero (LBACZ): If the command has the Namespace Zeroes (NSZ) bit set to ‘1’ and<br>completes successfully, then this bit is defined as follows:<br>Value Definition<br>The number of logical blocks specified by the Number of Logical Blocks (NLB) field have<br>0b<br>been cleared to zero.<br>1b All logical blocks in the entire namespace have been cleared to zero.|||


||Value|||Definition||
|---|---|---|---|---|---|
|0b|||The number of logical blocks specified by the Number of Logical Blocks (NLB) field have<br>been cleared to zero.|||
|1b|||All logical blocks in the entire namespace have been cleared to zero.|||

63

**Figure 88: Write Zeroes – Command Specific Status Values**

**Value**

**Definition**

81h
Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 82) settings
specified in the command are invalid for the Protection Information with which the namespace was
formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the ILBRT field is invalid
(refer to section 5.3.3).

82h

**Attempted Write to Read Only Range: The LBA range specified contains read-only blocks. The**
controller shall not return this status value if the read-only condition on the media is a result of a change
in the write protection state of a namespace (refer to the Namespace Write Protection section in the NVM

**Express Base Specification).**


||Value|||Definition||
|---|---|---|---|---|---|
|81h|||Invalid Protection Information: The Protection Information (PRINFO) field (refer to Figure 82) settings<br>specified in the command are invalid for the Protection Information with which the namespace was<br>formatted (refer to the PI field in Figure 90 and the DPS field in Figure 114) or the ILBRT field is invalid<br>(refer to section 5.3.3).|||
|82h|||Attempted Write to Read Only Range: The LBA range specified contains read-only blocks. The<br>controller shall not return this status value if the read-only condition on the media is a result of a change<br>in the write protection state of a namespace (refer to the Namespace Write Protection section in the NVM<br>Express Base Specification).|||

