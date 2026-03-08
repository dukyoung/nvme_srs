NVM Express [®] Base Specification, Revision 2.2


**7 I/O Commands**


An I/O command is a command submitted to an I/O Submission Queue. Figure 556 lists the I/O commands
that are defined for use in all I/O Command Sets. The following subsections provide definitions for each
command. Refer to section 3.1.3.4 for mandatory, optional, and prohibited I/O commands for the various
controller types. The following subsections describe the definition for each of these commands.


The user data format and any end-to-end protection information is I/O Command Set specific. Refer to each
I/O Command Set specification for applicability and additional details, if any. Refer to the referenced I/O
Command Set specification for all I/O Command Set specific commands described in Figure 556.


Commands shall only be submitted by the host when the controller is ready as indicated in the Controller
Status property (CSTS.RDY) and after appropriate I/O Submission Queue(s) and I/O Completion Queue(s)
have been created.


The submission queue entry (SQE) structure and the fields that are common to all I/O commands are
defined in section 4.1. The completion queue entry (CQE) structure and the fields that are common to all
I/O commands are defined in section 4.2. The command specific fields in the SQE and CQE structures (i.e.,
SQE Command Dwords 10-15, CQE Dword 0, and CQE Dword 1) for I/O commands supported across all
I/O Command Sets are defined in this section.


**Figure 556: Opcodes for I/O Commands**









|Opcode by Field|Col2|Combined<br>1<br>Opcode|2<br>Command|Reference|
|---|---|---|---|---|
|**(07:02)**|**(01:00)**|**(01:00)**|**(01:00)**|**(01:00)**|
|**Function**|**Data Transfer3 **|**Data Transfer3 **|**Data Transfer3 **|**Data Transfer3 **|
|0000 00b|00b|00h|Flush4|7.2|
|0000 11b|01b|0Dh|Reservation Register|7.6|
|0000 11b|10b|0Eh|Reservation Report|7.8|
|0001 00b|01b|11h|Reservation Acquire|7.5|
|0001 00b|10b|12h|I/O Management Receive|7.3|
|0001 01b|01b|15h|Reservation Release|7.7|
|0001 10b|00b|18h|Cancel4|7.1|
|0001 11b|01b|1Dh|I/O Management Send|7.4|
|0111 11b|11b5|7Fh|Fabric Commands5|6|
|**_Vendor Specific_**|**_Vendor Specific_**|**_Vendor Specific_**|**_Vendor Specific_**|**_Vendor Specific_**|
|1xxx xxb|NOTE 3|80h to FFh|Vendor specific||
|Notes:<br>1.<br>Opcodes not listed are I/O Command Set specific or reserved. Refer to Figure 91 for Opcode details.<br>2.<br>All I/O commands use the Namespace Identifier (NSID) field. The value FFFFFFFFh is not supported in this field<br>unless footnote 4 in this figure indicates that a specific command does support that value.<br>3.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = bidirectional. Refer to the Transfer<br>Direction field in Figure 91.<br>4.<br>This command may support the use of the Namespace Identifier (NSID) field set to FFFFFFFFh.<br>5.<br>All Fabrics commands use the opcode 7Fh with the direction of data transfer specified as shown in Figure 541.<br>Refer to section 6 for details.|Notes:<br>1.<br>Opcodes not listed are I/O Command Set specific or reserved. Refer to Figure 91 for Opcode details.<br>2.<br>All I/O commands use the Namespace Identifier (NSID) field. The value FFFFFFFFh is not supported in this field<br>unless footnote 4 in this figure indicates that a specific command does support that value.<br>3.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = bidirectional. Refer to the Transfer<br>Direction field in Figure 91.<br>4.<br>This command may support the use of the Namespace Identifier (NSID) field set to FFFFFFFFh.<br>5.<br>All Fabrics commands use the opcode 7Fh with the direction of data transfer specified as shown in Figure 541.<br>Refer to section 6 for details.|Notes:<br>1.<br>Opcodes not listed are I/O Command Set specific or reserved. Refer to Figure 91 for Opcode details.<br>2.<br>All I/O commands use the Namespace Identifier (NSID) field. The value FFFFFFFFh is not supported in this field<br>unless footnote 4 in this figure indicates that a specific command does support that value.<br>3.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = bidirectional. Refer to the Transfer<br>Direction field in Figure 91.<br>4.<br>This command may support the use of the Namespace Identifier (NSID) field set to FFFFFFFFh.<br>5.<br>All Fabrics commands use the opcode 7Fh with the direction of data transfer specified as shown in Figure 541.<br>Refer to section 6 for details.|Notes:<br>1.<br>Opcodes not listed are I/O Command Set specific or reserved. Refer to Figure 91 for Opcode details.<br>2.<br>All I/O commands use the Namespace Identifier (NSID) field. The value FFFFFFFFh is not supported in this field<br>unless footnote 4 in this figure indicates that a specific command does support that value.<br>3.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = bidirectional. Refer to the Transfer<br>Direction field in Figure 91.<br>4.<br>This command may support the use of the Namespace Identifier (NSID) field set to FFFFFFFFh.<br>5.<br>All Fabrics commands use the opcode 7Fh with the direction of data transfer specified as shown in Figure 541.<br>Refer to section 6 for details.|Notes:<br>1.<br>Opcodes not listed are I/O Command Set specific or reserved. Refer to Figure 91 for Opcode details.<br>2.<br>All I/O commands use the Namespace Identifier (NSID) field. The value FFFFFFFFh is not supported in this field<br>unless footnote 4 in this figure indicates that a specific command does support that value.<br>3.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = bidirectional. Refer to the Transfer<br>Direction field in Figure 91.<br>4.<br>This command may support the use of the Namespace Identifier (NSID) field set to FFFFFFFFh.<br>5.<br>All Fabrics commands use the opcode 7Fh with the direction of data transfer specified as shown in Figure 541.<br>Refer to section 6 for details.|


**7.1** **Cancel command**


The Cancel command is used to request an abort for specified commands submitted on the same I/O
Submission Queue to which the Cancel command is submitted. The Cancel command may apply to a single
namespace or to multiple namespaces. The Cancel command may be deeply queued. Some of the
commands to abort may have already completed, currently be processing, or be deeply queued. As a result,
the performance of the Cancel command may be impacted.


456


NVM Express [®] Base Specification, Revision 2.2


To abort an Admin command, the host uses the Abort command (refer to section 5.1.1). To abort a Cancel
command, the host may:


  - use the Abort command;

  - use a second Cancel command with a Cancel Action set to Single Command Cancel (i.e., 00b) that
specifies the CID of the Cancel command to abort; or

  - follow the procedure described in section 3.3.1.3 to delete the I/O Submission Queue and recreate
the I/O Submission Queue.


The controller applies the specified Cancel Action (refer to Figure 558) to all outstanding commands that
have been fetched prior to the processing of the Cancel command. The controller may or may not apply
the specified Cancel Action to commands that are fetched:


  - after the start of processing of the Cancel command; and

  - before the completion of the Cancel command.


There is no requirement to apply the specified Cancel Action to commands that have not been fetched by
the controller.


If an abort action is performed on a command to abort, that action may be:

  - an immediate abort (i.e., the abort action occurs prior to posting the completion queue entry for the
Cancel command); or

  - a deferred abort (i.e., the abort action may or may not occur prior to posting the completion queue
entry for the Cancel command).


For each command on which an immediate abort is performed, the controller shall meet the immediate
abort requirements (refer to section 5.1.1.1) for that command before posting the completion queue entry
for the Cancel command.


For each command on which a deferred abort is performed, there are no requirements on the ordering of
posting of the completion queue entry for the Cancel command (refer to section 7.1.1).


For each command on which an abort action is performed (i.e., immediate abort or deferred abort) the
status code shall be set to Command Abort Requested in the completion queue entry for that command.


If the Cancel command is supported, then the Commands Supported and Effects log page shall be
supported.


The Cancel command uses the Command Dword 10 and Command Dword 11 fields. All other command
specific fields are reserved.


**Figure 557: Cancel – Command Dword 10**





|Bits|Description|
|---|---|
|31:16|**Command Identifier (CID):**This field specifies the command identifier of the command to be aborted<br>(i.e., the CDW0.CID field within the command to be aborted).<br>If the Action Code field is set to Single Command Cancel and this field is set to the CID for this Cancel<br>command, then the controller shall abort the command with a status code of Invalid Command ID.<br>If the Action Code field is set to Multiple Command Cancel and this field is not set to FFFFh, then the<br>controller shall abort the command with a status code of Invalid Field in Command.|
|15:00|**Submission Queue Identifier (SQID):**This field specifies the identifier of the Submission Queue that<br>the Cancel command is associated with.<br>If the SQID does not match the Submission Queue Identifier of the submission queue to which the Cancel<br>command is submitted, then the controller shall abort the command with a status code of Invalid Field in<br>Command.|


457


NVM Express [®] Base Specification, Revision 2.2


**Figure 558: Cancel – Command Dword 11**









|Bits|Description|
|---|---|
|31:02|Reserved|
|01:00|**Action Code (ACODE):**<br>**Value**<br>**Cancel Action**<br>00b<br>**Single Command Cancel:** The hosts requests that the controller abort the<br>specific command submitted to the specified namespace with the specified CID.<br>If the NSID field is set to FFFFFFFFh then, the host requests that the controller<br>abort the specific command submitted to any NSID with the specified CID.<br>If the NSID is not set to FFFFFFFFh and the specified CID is not associated with<br>the specified NSID then, the controller shall abort the Cancel command with a<br>status code of Invalid Field in Command.<br>If the specified CID is not found, then the controller shall complete the Cancel<br>command with the Commands Eligible for Deferred Abort field cleared to 0h and<br>the Commands Aborted field cleared to 0h.<br>01b<br>**Multiple Command Cancel:** The hosts requests that the controller abort all<br>commands, other than this Cancel command, on the I/O Submission Queue to<br>which the Cancel command was submitted that were submitted to the specified<br>NSID.<br>If the NSID is set to FFFFFFFFh then the host requests that the controller abort<br>all commands, other than this Cancel command, submitted to the I/O Submission<br>Queue to which the Cancel command was submitted for all namespaces.<br>All others<br>Reserved|


|Value|Cancel Action|
|---|---|
|00b|**Single Command Cancel:** The hosts requests that the controller abort the<br>specific command submitted to the specified namespace with the specified CID.<br>If the NSID field is set to FFFFFFFFh then, the host requests that the controller<br>abort the specific command submitted to any NSID with the specified CID.<br>If the NSID is not set to FFFFFFFFh and the specified CID is not associated with<br>the specified NSID then, the controller shall abort the Cancel command with a<br>status code of Invalid Field in Command.<br>If the specified CID is not found, then the controller shall complete the Cancel<br>command with the Commands Eligible for Deferred Abort field cleared to 0h and<br>the Commands Aborted field cleared to 0h.|
|01b|**Multiple Command Cancel:** The hosts requests that the controller abort all<br>commands, other than this Cancel command, on the I/O Submission Queue to<br>which the Cancel command was submitted that were submitted to the specified<br>NSID.<br>If the NSID is set to FFFFFFFFh then the host requests that the controller abort<br>all commands, other than this Cancel command, submitted to the I/O Submission<br>Queue to which the Cancel command was submitted for all namespaces.|
|All others|Reserved|


**Command Completion**


Upon completion of the Cancel command, the controller posts a completion queue entry to the I/O
Completion Queue indicating the status for the Cancel command.


If the Cancel Action (refer to Figure 558) specified a Single Command Cancel Action and the Commands
Aborted field is cleared to 0h, then the host should examine the status in the completion queue entry of the
command to abort to determine whether the command was aborted or not (i.e., whether a deferred abort
was performed or not).


If the Cancel Action specified a Multiple Command Cancel Action, then the host should examine the status
in the completion queue entry of each command to abort to determine whether the command was aborted
or not.


Cancel command specific status code values are defined in Figure 559.


**Figure 559: Cancel – Command Specific Status Values**

|Value|Definition|
|---|---|
|84h|**Invalid Command ID:**The specified CID matched the CID of this Cancel command.|



Dword 0 of the completion queue entry contains information about the number of commands that were
aborted by this command. Dword 0 of the completion queue entry is defined in Figure 560.


458


NVM Express [®] Base Specification, Revision 2.2


**Figure 560: Cancel – Completion Queue Entry Dword 0**






|Bits|Description|
|---|---|
|31:16|**Commands Eligible for Deferred Abort (CEDA):** This field indicates the number of commands that match<br>the specified criteria (refer to Figure 557 and Figure 558) on which a deferred abort may be performed. A <br>value of 0h indicates that no commands are eligible for a deferred abort or that the controller does not<br>support deferred aborts. A value of FFFFh indicates that FFFFh or more commands are eligible for a<br>deferred abort.<br>If the Cancel Action (refer to Figure 558) specified a Single Command Cancel and an immediate abort was<br>performed on the specified command, then this field shall be cleared to 0h.|
|15:00|**Commands Aborted (CMDA):** This field indicates the number of commands on which the controller<br>performed an immediate abort as a result of processing this Cancel command. A value of 0h indicates that<br>the controller did not perform an immediate abort on any commands as a result of processing this Cancel<br>command.<br>If the Cancel Action (refer to Figure 558) specified a Single Command Cancel and an immediate abort was<br>performed on the specified command, then this field shall be set to 1h.|



**7.2** **Flush command**


The Flush command is used to request that the contents of volatile write cache be made non-volatile.


If a volatile write cache is enabled (refer to section 5.1.25.1.4), then the Flush command shall commit data
and metadata associated with the specified namespace(s) to non-volatile storage media. The flush applies
to all commands for the specified namespace(s) completed by the controller prior to the submission of the
Flush command. The controller may also flush additional data and/or metadata from any namespace.


If the Flush Behavior (FB) field is set to 11b in the VWC field in the Identify Controller data structure (refer
to Figure 313) and the specified NSID is FFFFFFFFh, then the Flush command applies to all namespaces
attached to the controller processing the Flush command. If the FB field is set to 10b and the specified
NSID is FFFFFFFFh, then the controller aborts the command with a status code of Invalid Namespace or
Format. If the FB field is cleared to 00b, then the controller behavior if the specified NSID is FFFFFFFFh is
not indicated. Controllers compliant with NVM Express Base Specification, Revision 1.4 and later shall not
set the FB field to the value of 00b.


If a namespace exists in an Endurance Group that has:

  - Flexible Data Placement (refer to section 8.1.10) enabled; and

  - the Volatile Write Cache Not Present (VWCNP) bit set to ‘1’ in the I/O Command Set Independent
Identify Namespace data structure (refer to Figure 320),


then, even though the Volatile Write Cache field in the Identify Controller data structure (refer to Figure 313)
indicates the presence of a volatile write cache in the controller, this namespace does not have a volatile
write cache present.


A host may use the Volatile Write Cache Not Present (VWCNP) bit in the I/O Command Set Independent
Identify Namespace data structure to determine if a Volatile Write Cache is not present for a namespace.


If a volatile write cache is not present or not enabled, then Flush commands shall have no effect and:


a) shall complete successfully if a sanitize operation is not in progress; and
b) may complete successfully if a sanitize operation is in progress.


All command specific fields are reserved.


**Command Completion**


Upon completion of the Flush command, the controller posts a completion queue entry to the associated
I/O Completion Queue.


459


NVM Express [®] Base Specification, Revision 2.2


**7.3** **I/O Management Receive command**


The I/O Management Receive command is used to receive information from the controller used by the host
to manage I/O. The behavior of the command is dependent on the specified operation as defined in the
Management Operation field in Figure 562.


The command uses the Data Pointer, Command Dword 10, and Command Dword 11 fields. All other
command specific fields are reserved. If the command uses PRPs for the data transfer, then the PRP Entry
1 and PRP Entry 2 fields are used. If the command uses SGLs for the data transfer, then the SGL Entry 1
field is used. All other command specific fields are reserved.


If the Number of Dwords (NUMD) field corresponds to a length that is less than the size of the data structure
to be returned, then only that specified portion of the data structure is transferred. If the NUMD field
corresponds to a length that is greater than the size of the associated data structure, then the entire contents
of the data structure are transferred and no additional data is transferred, unless otherwise specified.


**Figure 561: I/O Management Receive – Data Pointer**

|Bits|Description|
|---|---|
|127:00|**Data Pointer (DPTR):** This field specifies the location of a data buffer where data is transferred from.<br>Refer to Figure 92 for the definition of this field.|



**Figure 562: I/O Management Receive – Command Dword 10**





|Bits|Description|
|---|---|
|31:16|**Management Operation Specific (MOS):** This definition of this field is specific the value of the MO field.<br>If this field is not defined for the management operation specified by the MO field, then this field is<br>reserved.|
|15:08|Reserved|
|07:00|**Management Operation (MO):**This field specifies the management operation to perform.<br>**Value**<br>**Definition**<br>00h<br>No action<br>01h<br>**Reclaim Unit Handle Status:**For each Placement Handle of the namespace, the<br>controller shall return a Reclaim Unit Handle Status Descriptor for each Reclaim Group.<br>FFh<br>Vendor specific<br>All others<br>Reserved|


|Value|Definition|
|---|---|
|00h|No action|
|01h|**Reclaim Unit Handle Status:**For each Placement Handle of the namespace, the<br>controller shall return a Reclaim Unit Handle Status Descriptor for each Reclaim Group.|
|FFh|Vendor specific|
|All others|Reserved|


**Figure 563: I/O Management Receive – Command Dword 11**



|Bits|Description|
|---|---|
|31:00|**Number of Dwords (NUMD):**This field specifies the number of dwords to transfer. This is a 0’s based<br>value.|


**I/O Management Receive Operations**


**Reclaim Unit Handle Status (Management Operation 01h)**


The Reclaim Unit Handle Status management operation is used to provide information about Reclaim Unit
Handles (refer to section 1.5.84) that are accessible by the specified namespace. The returned data
contains one or more Reclaim Unit Handle Status Descriptor data structures (refer to the applicable I/O
Command Set specification). The information contained in each Reclaim Unit Handle Status Descriptor:

  - is the information at the time the controller processes that Reclaim Unit Handle Status Descriptor;
and

  - may or may not contain the information reflecting any outstanding command that affects the
reported Reclaim Unit Handle Status Descriptor.


If Flexible Data Placement is disabled in the Endurance Group containing the specified namespace, then
the command shall be aborted with a status code of FDP Disabled.


460


NVM Express [®] Base Specification, Revision 2.2


If the NSID field is set to 0h or FFFFFFFFh, then the controller shall abort the command with a status code
of Invalid Namespace or Format.


If the Number of Dwords (NUMD) field corresponds to a length that is greater than the size of the Reclaim
Unit Handle Status data structure (refer to Figure 564), then the entire contents of the data structure are
transferred and zeroes are transferred beyond the end of that data structure.


**Figure 564: Reclaim Unit Handle Status**














|Bytes|Description|
|---|---|
|**Header**|**Header**|
|13:00|Reserved|
|15:14|**Number of Reclaim Unit Handle Status Descriptors (NRUHSD):**This field indicates the<br>number of Reclaim Unit Handle Status Descriptors in the Reclaim Unit Handle Status<br>Descriptor list.|
|**Reclaim Unit Handle Status Descriptor List**|**Reclaim Unit Handle Status Descriptor List**|
|47:16|**Reclaim Unit Handle Status Descriptor 1:**The first Reclaim Unit Handle Status<br>Descriptor (refer to the applicable I/O Command Set specification).|
|79:48|**Reclaim Unit Handle Status Descriptor 2:**The second Reclaim Unit Handle Status<br>Descriptor (refer to the applicable I/O Command Set specification), if any.|
|…|…|
|(NRUHSD *32)+15:<br>(NRUHSD *32)–16|**Reclaim Unit Handle Status Descriptor NRUHSD:**The last Reclaim Unit Handle Status<br>Descriptor (refer to the applicable I/O Command Set specification), if any.|



The Reclaim Unit Handle Status Descriptors are defined in the I/O Command Set specifications, if
supported.


**Command Completion**


When the command is completed with success or failure, the controller shall post a completion queue entry
to the associated I/O Completion Queue indicating the status for the command.


**7.4** **I/O Management Send command**


The I/O Management Send command is used to manage I/O and the behavior of the command is dependent
on the specified operation as defined in the Management Operation field in Figure 566.


The command uses the Data Pointer and Command Dword 10 field. All other command specific fields are
reserved. If the command uses PRPs for the data transfer, then the PRP Entry 1 and PRP Entry 2 fields
are used. If the command uses SGLs for the data transfer, then the SGL Entry 1 field is used. All other
command specific fields are reserved.


**Figure 565: I/O Management Send – Data Pointer**

|Bits|Description|
|---|---|
|127:00|**Data Pointer (DPTR):** This field specifies the location of a data buffer where data is transferred from.<br>Refer to Figure 92 for the definition of this field.|



**Figure 566: I/O Management Send – Command Dword 10**

|Bits|Description|
|---|---|
|31:16|**Management Operation Specific (MOS):** The definition of this field is specific to the value of the MO<br>field. If this field is not defined for the management operation specified by the MO field, then this field is<br>reserved.|
|15:08|Reserved|



461


NVM Express [®] Base Specification, Revision 2.2


**Figure 566: I/O Management Send – Command Dword 10**






|Bits|Description|
|---|---|
|07:00|**Management Operation (MO):**This field specifies the management operation to perform.<br>**Value**<br>**Definition**<br>00h<br>No action<br>01h<br>**Reclaim Unit Handle Update:** Update the reference to the Reclaim Unit specified by<br>each entry in the Placement Identifier list to reference an empty Reclaim Unit (refer to<br>section 3.2.4).<br>FFh<br>Vendor specific<br>All others<br>Reserved|


|Value|Definition|
|---|---|
|00h|No action|
|01h|**Reclaim Unit Handle Update:** Update the reference to the Reclaim Unit specified by<br>each entry in the Placement Identifier list to reference an empty Reclaim Unit (refer to<br>section 3.2.4).|
|FFh|Vendor specific|
|All others|Reserved|



**I/O Management Send Operations**


**Reclaim Unit Handle Update (Management Operation 01h)**


The Reclaim Unit Handle Update management operation for the I/O Management Send command provides
a list of Placement Identifiers (refer to Figure 568). The number of Placement Identifiers is defined in the
Management Operation Specific field defined in Figure 567. For each Placement Identifier in the list:

  - If the currently referenced Reclaim Unit has been written with user data, then the Placement
Identifier shall be modified to reference a different Reclaim Unit that is empty (refer to section 3.2.4);
and

  - If the currently referenced Reclaim Unit has not been written with any user data (i.e., is already
empty), then the Placement Identifier may be modified to reference a different Reclaim Unit that is
empty.


**Figure 567: Management Operation Specific – Reclaim Unit Handle Update Operation**






|Bits|Description|
|---|---|
|15:00|**Number of Placement Identifiers (NPID):** Indicates the number of Placement Identifiers that are<br>specified in the command. This is a 0’s based value.<br>This field shall not exceed the minimum of:<br>• <br>the value in the Max Placement Identifiers (MAXPIDS) field of the enabled FDP configuration<br>(refer to Figure 281); and<br>• <br>the product of the Number of Reclaim Groups (NRG) field and the Number of Reclaim Unit<br>Handles (NRUH) field of the enabled FDP configuration (refer to Figure 281);|



If a specified Placement Identifier is invalid due to:

  - the value of the Reclaim Group Identifier field being greater than or equal to the Number of Reclaim
Groups field of the FDP Configuration Descriptor (refer to Figure 281) for the Endurance Group
associated with the specified namespace; or

  - the specified Placement Handle field being greater than or equal to the Number of Placement
Handles field specified when the namespace was created,


then the controller shall abort the command with a status code of Invalid Field in Command.


If the value represented by the Number of Placement Identifiers (NPID) field is greater than the Max
Placement Identifiers (MAXPIDS) field (refer to Figure 281) in the current FDP configuration, then the
controller shall abort the command with a status code of Invalid Field in Command.


If the command is aborted, then Placement Identifiers may or may not have been updated.


While processing an I/O Management Send command that specifies the Reclaim Unit Handle Update
operation, if the controller processes a write command that utilizes a Placement Identifier specified in the
Placement Identifier List of that I/O Management Send command, then the controller may write the user
data for that write command to the referenced Reclaim Unit:


462


NVM Express [®] Base Specification, Revision 2.2


  - prior to processing that I/O Management Send command; or

  - upon the completion of that I/O Management Send command.


**Figure 568: Reclaim Unit Handle Update – Data Buffer**






|Bytes|Description|
|---|---|
|**Placement Identifier List**|**Placement Identifier List**|
|01:00|**Placement Identifier 1:** This field specifies the first Placement Identifier that indicates a Placement<br>Handle and a Reclaim Group Identifier. Refer to Figure 283 and Figure 284.|
|03:02|**Placement Identifier 2:**This field specifies the second Placement Identifier that indicates a<br>Placement Handle and a Reclaim Group Identifier, if any. Refer to Figure 283 and Figure 284.|
|…|…|
|(NPID*2)+1:<br>(NPID*2)|**Placement Identifier NPID:**This field specifies the last Placement Identifier that indicates a<br>Placement Handle and a Reclaim Group Identifier, if any. Refer to Figure 283 and Figure 284.|



If Flexible Data Placement is disabled in the Endurance Group containing the specified namespace, then
the controller shall abort the command with a status code of FDP Disabled.


**Command Completion**


When the command is completed with success or failure, the controller shall post a completion queue entry
to the associated I/O Completion Queue indicating the status for the command.


**7.5** **Reservation Acquire command**


The Reservation Acquire command is used to:

  - acquire a reservation on a namespace;

  - preempt a reservation held on a namespace; or

  - preempt a reservation held on a namespace and abort outstanding commands for that namespace.


The command uses Command Dword 10 and a Reservation Acquire data structure in memory. If the
command uses PRPs for the data transfer, then PRP Entry 1 and PRP Entry 2 fields are used. If the
command uses SGLs for the data transfer, then the SGL Entry 1 field is used. All other command specific
fields are reserved.


**Figure 569: Reservation Acquire – Data Pointer**

|Bits|Description|
|---|---|
|127:00|**Data Pointer (DPTR):** This field specifies the location of a data buffer where data is transferred from.<br>Refer to Figure 92 for the definition of this field.|



**Figure 570: Reservation Acquire – Command Dword 10**

|Bits|Description|
|---|---|
|31:16|Reserved|
|15:08|**Reservation Type (RTYPE):**This field specifies the type of reservation to be created. The field is defined<br>in Figure 572.|
|07:05|Reserved|



463


NVM Express [®] Base Specification, Revision 2.2


**Figure 570: Reservation Acquire – Command Dword 10**











|Bits|Description|
|---|---|
|04|**Dispersed Namespace Reservation Support (DISNSRS):** This bit specifies host support for<br>reservations on dispersed namespaces for a host that supports dispersed namespaces (i.e., for a host<br>that has set the Host Dispersed Namespace Support (HDISNS) field to 1h in the Host Behavior Support<br>feature).<br>If this bit is set to ‘1’, then the host supports reservations on dispersed namespaces (i.e., the host<br>supports receiving a value of FFFDh in the Controller ID (CNTLID) field of a Registered Controller data<br>structure or Registered Controller Extended data structure (refer to section 8.1.9.6)).<br>If this bit is cleared to ‘0’, then the host does not support reservations on dispersed namespaces (i.e.,<br>the host does not support receiving a value of FFFDh in the Controller ID (CNTLID) field of a Registered<br>Controller data structure or Registered Controller Extended data structure (refer to section 8.1.9.6)). If<br>the HDISNS field is set to 1h in the Host Behavior Support feature and the host submits the command<br>to a dispersed namespace with this bit cleared to ‘0’, then the controller aborts the command with a status<br>code of Namespace Is Dispersed as described in section 8.1.9.6.|
|03|**Ignore Existing Key (IEKEY)**: If this bit is set to a ‘1’, then the controller shall return an error of Invalid<br>Field in Command. If this bit is cleared to ‘0’, then the Current Reservation Key is checked.|
|02:00|**Reservation Acquire Action (RACQA):**This field specifies the action that is performed by the<br>command.<br>**Value**<br>**Definition**<br>**Reference**<br>000b<br>Acquire<br>8.1.22.5<br>001b<br>Preempt<br>8.1.22.7<br>010b<br>Preempt and Abort<br>8.1.22.7<br>011b to 111b<br>Reserved|


|Value|Definition|Reference|
|---|---|---|
|000b|Acquire|8.1.22.5|
|001b|Preempt|8.1.22.7|
|010b|Preempt and Abort|8.1.22.7|
|011b to 111b|Reserved|Reserved|


**Figure 571: Reservation Acquire Data Structure**







|Bytes|Description|
|---|---|
|07:00|**Current Reservation Key (CRKEY):** The field specifies the current reservation key associated with<br>the host.|
|15:08|**Preempt Reservation Key (PRKEY):** If the Reservation Acquire Action is set to 001b (i.e.,<br>Preempt) or 010b (i.e., Preempt and Abort), then this field specifies the reservation key to be<br>unregistered from the namespace. For all other Reservation Acquire Action values, this field is<br>reserved.|


**Figure 572: Reservation Type Encoding**


|Value|Definition|
|---|---|
|0h|Reserved|
|1h|Write Exclusive Reservation|
|2h|Exclusive Access Reservation|
|3h|Write Exclusive - Registrants Only Reservation|
|4h|Exclusive Access - Registrants Only Reservation|
|5h|Write Exclusive - All Registrants Reservation|
|6h|Exclusive Access - All Registrants Reservation|
|7h to FFh|Reserved|



**Command Completion**


When the command is completed, the controller shall post a completion queue entry to the associated I/O
Completion Queue indicating the status for the command.


**7.6** **Reservation Register command**


The Reservation Register command is used to register, unregister, or replace a reservation key.


464


NVM Express [®] Base Specification, Revision 2.2


The command uses Command Dword 10 and a Reservation Register data structure in memory (refer to
Figure 575). If the command uses PRPs for the data transfer, then PRP Entry 1 and PRP Entry 2 fields are
used. If the command uses SGLs for the data transfer, then the SGL Entry 1 field is used. All other command
specific fields are reserved.


**Figure 573: Reservation Register – Data Pointer**

|Bits|Description|
|---|---|
|127:00|**Data Pointer (DPTR):** This field specifies the location of a data buffer where data is transferred from.<br>Refer to Figure 92 for the definition of this field.|



**Figure 574: Reservation Register – Command Dword 10**








|Value|Definition|
|---|---|
|00b|No change to PTPL state|
|01b|Reserved|
|10b|Clear PTPL state to ‘0’. Reservations are released and registrants are cleared on a power on.|
|11b|Set PTPL state to ‘1’. Reservations and registrants persist across a power loss.|





|Bits|Description|
|---|---|
|31:30|**Change Persist Through Power Loss State (CPTPL):**This field allows the Persist Through Power Loss<br>(PTPL) state associated with the namespace to be modified as a side effect of processing this command. If<br>the Reservation Persistence feature (refer to section 5.1.25.1.30) is saveable, then any change to the PTPL<br>state as a result of processing this command shall be applied to both the current value and the saved value<br>of that feature.<br>**Value**<br>**Definition**<br>00b<br>No change to PTPL state<br>01b<br>Reserved<br>10b<br>Clear PTPL state to ‘0’. Reservations are released and registrants are cleared on a power on.<br>11b<br>Set PTPL state to ‘1’. Reservations and registrants persist across a power loss.|
|29:05|Reserved|
|04|**Dispersed Namespace Reservation Support (DISNSRS):** This bit specifies host support for reservations<br>on dispersed namespaces for a host that supports dispersed namespaces (i.e., for a host that has set the<br>Host Dispersed Namespace Support (HDISNS) field to 1h in the Host Behavior Support feature).<br>If this bit is set to ‘1’, then the host supports reservations on dispersed namespaces (i.e., the host supports<br>receiving a value of FFFDh in the Controller ID (CNTLID) field of a Registered Controller data structure or<br>Registered Controller Extended data structure (refer to section 8.1.9.6)).<br>If this bit is cleared to ‘0’, then the host does not support reservations on dispersed namespaces (i.e., the<br>host does not support receiving a value of FFFDh in the Controller ID (CNTLID) field of a Registered<br>Controller data structure or Registered Controller Extended data structure (refer to section 8.1.9.6)). If the<br>HDISNS field is set to 1h in the Host Behavior Support feature and the host submits the command to a<br>dispersed namespace with this bit cleared to ‘0’, then the controller aborts the command with a status code<br>of Namespace Is Dispersed as described in section 8.1.9.6.|
|03|**Ignore Existing Key (IEKEY)**: If this bit is set to a ‘1’, then Reservation Register Action (RREGA) field<br>values that use the Current Reservation Key (CRKEY) shall succeed regardless of the value of the Current<br>Reservation Key field in the command (i.e., the current reservation key, if any, is not checked, and absence<br>of a current reservation key does not cause an error).|
|02:00|**Reservation Register Action (RREGA):**This field specifies the registration action that is performed by the<br>command.<br>**Value**<br>**Definition**<br>**Reference**<br>000b<br>Register Reservation Key<br>8.1.22.3<br>001b<br>Unregister Reservation Key<br>8.1.22.4<br>010b<br>Replace Reservation Key<br>8.1.22.3<br>011b to 111b<br>Reserved|


|Value|Definition|Reference|
|---|---|---|
|000b|Register Reservation Key|8.1.22.3|
|001b|Unregister Reservation Key|8.1.22.4|
|010b|Replace Reservation Key|8.1.22.3|
|011b to 111b|Reserved|Reserved|


**Figure 575: Reservation Register Data Structure**







|Bytes|Description|
|---|---|
|07:00|**Current Reservation Key (CRKEY):** If the Reservation Register Action is 001b (i.e., Unregister<br>Reservation Key) or 010b (i.e., Replace Reservation Key), then this field contains the current reservation<br>key associated with the host. For all other Reservation Register Action values, this field is reserved. <br>The controller ignores the value of this field when the Ignore Existing Key (IEKEY) bit is set to ‘1’.|


465


NVM Express [®] Base Specification, Revision 2.2


**Figure 575: Reservation Register Data Structure**





|Bytes|Description|
|---|---|
|15:08|**New Reservation Key (NRKEY):** If the Reservation Register Action field is cleared to 000b (i.e., Register<br>Reservation Key) or 010b (i.e., Replace Reservation Key), then this field contains the new reservation key<br>associated with the host. For all other Reservation Register Action values, this field is reserved.|


**Command Completion**



When the command is completed, the controller shall post a completion queue entry to the associated I/O
Completion Queue indicating the status for the command.


**7.7** **Reservation Release command**


The Reservation Release command is used to release or clear a reservation held on a namespace.


The command uses Command Dword 10 and a Reservation Release data structure in memory. If the
command uses PRPs for the data transfer, then PRP Entry 1 and PRP Entry 2 fields are used. If the
command uses SGLs for the data transfer, then the SGL Entry 1 field is used. All other command specific
fields are reserved.


**Figure 576: Reservation Release – Data Pointer**

|Bits|Description|
|---|---|
|127:00|**Data Pointer (DPTR):** This field specifies the location of a data buffer where data is transferred from.<br>Refer to Figure 92 for the definition of this field.|



**Figure 577: Reservation Release – Command Dword 10**











|Bits|Description|
|---|---|
|31:16|Reserved|
|15:08|**Reservation Type (RTYPE):**If the Reservation Release Action field is cleared to 000b (i.e., Release),<br>then this field specifies the type of reservation that is being released. The reservation type in this field<br>shall match the current reservation type. If the reservation type in this field does not match the current<br>reservation type, then the controller should return a status code of Invalid Field in Command. This field<br>is defined in Figure 572.|
|07:05|Reserved|
|04|**Dispersed Namespace Reservation Support (DISNSRS):** This bit specifies host support for<br>reservations on dispersed namespaces for a host that supports dispersed namespaces (i.e., for a host<br>that has set the Host Dispersed Namespace Support (HDISNS) field to 1h in the Host Behavior Support<br>feature).<br>If this bit is set to ‘1’, then the host supports reservations on dispersed namespaces (i.e., the host<br>supports receiving a value of FFFDh in the Controller ID (CNTLID) field of a Registered Controller data<br>structure or Registered Controller Extended data structure (refer to section 8.1.9.6)).<br>If this bit is cleared to ‘0’, then the host does not support reservations on dispersed namespaces (i.e.,<br>the host does not support receiving a value of FFFDh in the Controller ID (CNTLID) field of a Registered<br>Controller data structure or Registered Controller Extended data structure (refer to section 8.1.9.6)). If<br>the HDISNS field is set to 1h in the Host Behavior Support feature and the host submits the command<br>to a dispersed namespace with this bit cleared to ‘0’, then the controller aborts the command with a status<br>code of Namespace Is Dispersed as described in section 8.1.9.6.|
|03|**Ignore Existing Key (IEKEY)**: If this bit is set to a ‘1’, then the controller shall return an error of Invalid<br>Field in Command. If this bit is cleared to ‘0’, then the Current Reservation Key is checked.|
|02:00|**Reservation Release Action (RRELA):**This field specifies the reservation action that is performed by<br>the command.<br>**Value**<br>**Definition**<br>**Reference**<br>000b<br>Release<br>8.1.22.6<br>001b<br>Clear<br>8.1.22.8<br>010b to 111b<br>Reserved|


|Value|Definition|Reference|
|---|---|---|
|000b|Release|8.1.22.6|
|001b|Clear|8.1.22.8|
|010b to 111b|Reserved|Reserved|


466


NVM Express [®] Base Specification, Revision 2.2


**Figure 578: Reservation Release Data Structure**

|Bytes|O/M|Description|
|---|---|---|
|7:0|M|**Current Reservation Key (CRKEY):** The field specifies the current reservation key<br>associated with the host.|



**Command Completion**


When the command is completed, the controller shall post a completion queue entry to the associated I/O
Completion Queue indicating the status for the command.


**7.8** **Reservation Report command**


The Reservation Report command returns a Reservation Status data structure to memory that describes
the registration and reservation status of a namespace.


If the namespace is not a dispersed namespace, then the size of the Reservation Status data structure is
a function of the number of registrants of the namespace (i.e., there is a Registrant data structure and/or
Registrant Extended data structure for each such registrant). If the namespace is a dispersed namespace
that is able to be accessed by controllers in multiple participating NVM subsystems, then the size of the
Reservation Status data structure is a function of the number of registrants of the namespace in the NVM
subsystem containing the controller processing the command and the number of registrants of the
namespace in each separate participating NVM subsystem. The controller returns the data structure in
Figure 582 if the host has selected a 64-bit Host Identifier and the data structure in Figure 583 if the host
has selected a 128-bit Host Identifier (refer to section 5.1.25.1.28).


For controllers compliant with NVM Express Base Specification, Revision 2.0 and earlier, registrants of the
namespace that are not associated with any controller in the NVM subsystem may or may not be reported
by this command.


If a 64-bit Host Identifier has been specified and the Extended Data Structure bit is set to ‘1’ in Command
Dword 11, then the controller shall abort the command with the status code of Host Identifier Inconsistent
Format. If a 128-bit Host Identifier has been specified and the Extended Data Structure bit is cleared to ‘0’
in Command Dword 11, then the controller shall abort the command with the status code of Host Identifier
Inconsistent Format.


The command uses Command Dword 10 and Command Dword 11. If the command uses PRPs for the
data transfer, then PRP Entry 1 and PRP Entry 2 fields are used. If the command uses SGLs for the data
transfer, then the SGL Entry 1 field is used. All other command specific fields are reserved.


**Figure 579: Reservation Report – Data Pointer**

|Bits|Description|
|---|---|
|127:00|**Data Pointer (DPTR):** This field specifies the location of a data buffer where data is transferred to. Refer<br>to Figure 92 for the definition of this field.|



**Figure 580: Reservation Report – Command Dword 10**





|Bits|Description|
|---|---|
|31:00|**Number of Dwords (NUMD):**This field specifies the number of dwords of the Reservation Status data<br>structure to transfer. This is a 0’s based value.<br>If this field corresponds to a length that is less than the size of the Reservation Status data structure,<br>then only that specified portion of the data structure is transferred. If this field corresponds to a length<br>that is greater than the size of the Reservation Status data structure, then the entire contents of the data<br>structure are transferred and no additional data is transferred.|


467


NVM Express [®] Base Specification, Revision 2.2


**Figure 581: Reservation Report – Command Dword 11**





|Bits|Description|
|---|---|
|31:02|Reserved|
|01|**Dispersed Namespace Reservation Support (DISNSRS):** This bit specifies host support for<br>reservations on dispersed namespaces for a host that supports dispersed namespaces (i.e., for a host<br>that has set the Host Dispersed Namespace Support (HDISNS) field to 1h in the Host Behavior Support<br>feature).<br>If this bit is set to ‘1’, then the host supports reservations on dispersed namespaces (i.e., the host<br>supports receiving a value of FFFDh in the Controller ID (CNTLID) field of a Registrant data structure or<br>Registrant Extended data structure (refer to section 8.1.9.6)).<br>If this bit is cleared to ‘0’, then the host does not support reservations on dispersed namespaces (i.e.,<br>the host does not support receiving a value of FFFDh in the Controller ID (CNTLID) field of a Registrant<br>data structure or Registrant Extended data structure (refer to section 8.1.9.6)). If the HDISNS field is set<br>to 1h in the Host Behavior Support feature and the host submits the command to a dispersed namespace<br>with this bit cleared to ‘0’, then the controller aborts the command with a status code of Namespace Is<br>Dispersed as described in section 8.1.9.6.|
|00|**Extended Data Structure (EDS):**If this bit is set to ‘1’, then the controller returns the extended data<br>structure defined in Figure 583. If this bit is cleared to ‘0’, then the controller returns the data structure<br>defined in Figure 582.|


**Figure 582: Reservation Status Data Structure**










|Value|Definition|
|---|---|
|0|Reservations are released and registrants are cleared on a power on.|
|1|Reservations and registrants persist across a power loss.|








|Bytes|Description|
|---|---|
|**Header**|**Header**|
|03:00|**Generation (GEN):**This field contains a 32-bit wrapping counter that is incremented any time any<br>one the following occur:<br>• <br>a Reservation Register command completes successfully on any controller associated with<br>the namespace; <br>• <br>a Reservation Release command with Reservation Release Action (RRELA) set to 001b (i.e.,<br>Clear) completes successfully on any controller associated with the namespace; and <br>• <br>a Reservation Acquire command with Reservation Acquire Action (RACQA) set to 001b<br>(Preempt) or 010b (Preempt and Abort) completes successfully on any controller associated<br>with the namespace. <br>If the value of this field is FFFFFFFFh, then the field shall be cleared to 0h when incremented (i.e.,<br>rolls over to 0h).|
|04|**Reservation Type (RTYPE):**This field indicates whether a reservation is held on the namespace. A<br>value of 0h indicates that no reservation is held on the namespace. A non-zero value indicates a<br>reservation is held on the namespace and the reservation type is defined in Figure 572.|
|06:05|**Number of Registrants (REGSTRNT):**This field indicates the number of registrants of the<br>namespace. This indicates the number of Registrant data structures or Registrant Extended data<br>structures contained in this data structure.<br>Note: This field was formerly named Number of Registered Controllers (REGCTL).|
|08:07|Reserved|
|09|**Persist Through Power Loss State (PTPLS):**This field indicates the Persist Through Power Loss<br>State associated with the namespace.<br>**Value**<br>**Definition**<br>0 <br>Reservations are released and registrants are cleared on a power on.<br>1 <br>Reservations and registrants persist across a power loss.|
|23:10|Reserved|
|**Registered Controller Data Structure List**|**Registered Controller Data Structure List**|
|47:24|**Registrant Data Structure 0**<br>Note: This field was formerly named Registered Controller Data Structure 0.|
|…|…|



468


NVM Express [®] Base Specification, Revision 2.2


**Figure 582: Reservation Status Data Structure**

|Bytes|Description|
|---|---|
|24*n+47:<br>24*(n+1)|**Registrant Data Structure n**|



**Figure 583: Reservation Status Extended Data Structure**










|Bytes|Description|
|---|---|
|**Header**|**Header**|
|23:00|**Reservation Status Header (RSHDR):**Refer to the Reservation Status Header in Figure 582 for<br>definition.|
|63:24|Reserved|
|**Registered Controller Extended Data Structure List**|**Registered Controller Extended Data Structure List**|
|127:64|**Registrant Extended Data Structure 0**<br>Note: This field was formerly named Registered Controller Extended Data Structure 0.|
|…|…|
|64*(n+1)+63:<br>64*(n+1)|**Registrant Extended Data Structure n**|



**Figure 584: Registered Controller Data Structure**







|Bytes|Description|
|---|---|
|01:00|**Controller ID (CNTLID):**If a registrant of the namespace is associated with a controller in the NVM<br>subsystem, then this field contains the controller ID (i.e., the value of the CNTLID field in the Identify<br>Controller data structure) of the controller that is associated with the registrant whose host identifier<br>is indicated in the Host identifier field of this Registrant data structure.<br>If a registrant of the namespace is not associated with any controller in the NVM subsystem, then the<br>controller processing the command shall set this field to FFFFh.<br>If the namespace is a dispersed namespace and the controller is not contained in the same<br>participating NVM subsystem as the controller processing the command, then the Controller ID field<br>is set to FFFDh, as described in section 8.1.9.6.|
|02|**Reservation Status (RCSTS):**This field indicates the reservation status of the registrant associated<br>with this data structure (i.e., the registrant whose host identifier is indicated in the Host Identifier field<br>of this Registrant data structure).<br>**Bits**<br>**Description**<br>7:1<br>Reserved<br>0 <br>**Association with Host Holding Reservation (AHHR):** If this bit is set to '1', then the<br>registrant associated with this data structure holds a reservation on the namespace. If<br>this bit is cleared to ‘0’, then the controller is not associated with a host that holds a<br>reservation on the namespace.|
|07:03|Reserved|
|15:08|**Host Identifier (HOSTID):** This field contains the 64-bit Host Identifier of the registrant of the<br>namespace described by this data structure.|
|23:16|**Reservation Key (RKEY):** This field contains the reservation key of the registrant described by this<br>data structure.|


|Bits|Description|
|---|---|
|7:1|Reserved|
|0|**Association with Host Holding Reservation (AHHR):** If this bit is set to '1', then the<br>registrant associated with this data structure holds a reservation on the namespace. If<br>this bit is cleared to ‘0’, then the controller is not associated with a host that holds a<br>reservation on the namespace.|


**Figure 585: Registered Controller Extended Data Structure**

|Bytes|Description|
|---|---|
|01:00|**Controller ID (CNTLID):**Refer to Figure 584 for definition.|
|02|**Reservation Status (RCSTS):**Refer to Figure 584 for definition.|
|07:03|Reserved|
|15:08|**Reservation Key (RKEY):** Refer to Figure 584 for definition.|



469


NVM Express [®] Base Specification, Revision 2.2


**Figure 585: Registered Controller Extended Data Structure**

|Bytes|Description|
|---|---|
|31:16|**Host Identifier (HOSTID):** This field contains the 128-bit Host Identifier of the registrant of the<br>namespace described by this data structure.|
|63:32|Reserved|



**Command Completion**


When the command is completed, the controller shall post a completion queue entry to the associated I/O
Completion Queue indicating the status for the command.


470


