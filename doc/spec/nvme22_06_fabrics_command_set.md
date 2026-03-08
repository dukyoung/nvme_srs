NVM Express [®] Base Specification, Revision 2.2


**6 Fabrics Command Set**


Fabrics commands are used to create queues and initialize a controller. Fabrics commands have an
Opcode field of 7Fh and are distinguished by the Fabrics Command Type as shown in Figure 541. Fabrics
commands are processed regardless of the state of controller enable (CC.EN). The Fabrics command
capsule is defined in section 3.3.2.1.1 and the Fabrics response capsule and status is defined in section
3.3.2.1.2. The common Fabrics Submission Queue entry is shown in Figure 94 and the common Fabrics
Completion Queue entry is shown in Figure 99.


Restrictions on processing commands listed in Figure 541 are defined in the Admin Command Set in
section 5 (e.g., while the NVM subsystem is performing a sanitize operation or processing of a Format NVM
command).


**Figure 541: Fabrics Command Type**















|Some Fabric Command Type by<br>Field|Col2|Combined<br>Fabrics<br>Command<br>2<br>Type|1<br>O/M|3<br>I/O Queue|Command|
|---|---|---|---|---|---|
|**(07:02)**|**(01:00)**|**(01:00)**|**(01:00)**|**(01:00)**|**(01:00)**|
|**Function**|**Data Transfer4 **|**Data Transfer4 **|**Data Transfer4 **|**Data Transfer4 **|**Data Transfer4 **|
|0000 00b|00b|00h|M|No|Property Set|
|0000 00b|01b|01h|M|Yes|Connect5|
|0000 01b|00b|04h|M|No|Property Get|
|0000 01b|01b|05h|O|Yes|Authentication Send|
|0000 01b|10b|06h|O|Yes|Authentication Receive|
|0000 10b|00b|08h|O|Yes|Disconnect|
|**_Vendor Specific_**|**_Vendor Specific_**|**_Vendor Specific_**|**_Vendor Specific_**|**_Vendor Specific_**|**_Vendor Specific_**|
|11xx xxb|Note 4|C0h to FFh|O||Vendor specific|
|Notes:<br>1.<br>O/M definition: O = Optional, M = Mandatory.<br>2.<br>Fabrics Command Types not listed are reserved.<br>3.<br>All Fabrics commands, other than the Disconnect command, may be submitted on the Admin Queue. The I/O Queue<br>supports Fabrics commands as specified in this column. If a Fabrics command that is not supported on an I/O Queue<br>is sent on an I/O Queue, that command shall be aborted with a status code of Invalid Field in Command.<br>4.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = reserved. Refer to the Transfer<br>Direction field in Figure 94.<br>5.<br>The Connect command is submitted and completed on the same queue that the Connect command creates. Refer<br>to section 3.3.2.2.|Notes:<br>1.<br>O/M definition: O = Optional, M = Mandatory.<br>2.<br>Fabrics Command Types not listed are reserved.<br>3.<br>All Fabrics commands, other than the Disconnect command, may be submitted on the Admin Queue. The I/O Queue<br>supports Fabrics commands as specified in this column. If a Fabrics command that is not supported on an I/O Queue<br>is sent on an I/O Queue, that command shall be aborted with a status code of Invalid Field in Command.<br>4.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = reserved. Refer to the Transfer<br>Direction field in Figure 94.<br>5.<br>The Connect command is submitted and completed on the same queue that the Connect command creates. Refer<br>to section 3.3.2.2.|Notes:<br>1.<br>O/M definition: O = Optional, M = Mandatory.<br>2.<br>Fabrics Command Types not listed are reserved.<br>3.<br>All Fabrics commands, other than the Disconnect command, may be submitted on the Admin Queue. The I/O Queue<br>supports Fabrics commands as specified in this column. If a Fabrics command that is not supported on an I/O Queue<br>is sent on an I/O Queue, that command shall be aborted with a status code of Invalid Field in Command.<br>4.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = reserved. Refer to the Transfer<br>Direction field in Figure 94.<br>5.<br>The Connect command is submitted and completed on the same queue that the Connect command creates. Refer<br>to section 3.3.2.2.|Notes:<br>1.<br>O/M definition: O = Optional, M = Mandatory.<br>2.<br>Fabrics Command Types not listed are reserved.<br>3.<br>All Fabrics commands, other than the Disconnect command, may be submitted on the Admin Queue. The I/O Queue<br>supports Fabrics commands as specified in this column. If a Fabrics command that is not supported on an I/O Queue<br>is sent on an I/O Queue, that command shall be aborted with a status code of Invalid Field in Command.<br>4.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = reserved. Refer to the Transfer<br>Direction field in Figure 94.<br>5.<br>The Connect command is submitted and completed on the same queue that the Connect command creates. Refer<br>to section 3.3.2.2.|Notes:<br>1.<br>O/M definition: O = Optional, M = Mandatory.<br>2.<br>Fabrics Command Types not listed are reserved.<br>3.<br>All Fabrics commands, other than the Disconnect command, may be submitted on the Admin Queue. The I/O Queue<br>supports Fabrics commands as specified in this column. If a Fabrics command that is not supported on an I/O Queue<br>is sent on an I/O Queue, that command shall be aborted with a status code of Invalid Field in Command.<br>4.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = reserved. Refer to the Transfer<br>Direction field in Figure 94.<br>5.<br>The Connect command is submitted and completed on the same queue that the Connect command creates. Refer<br>to section 3.3.2.2.|Notes:<br>1.<br>O/M definition: O = Optional, M = Mandatory.<br>2.<br>Fabrics Command Types not listed are reserved.<br>3.<br>All Fabrics commands, other than the Disconnect command, may be submitted on the Admin Queue. The I/O Queue<br>supports Fabrics commands as specified in this column. If a Fabrics command that is not supported on an I/O Queue<br>is sent on an I/O Queue, that command shall be aborted with a status code of Invalid Field in Command.<br>4.<br>00b = no data transfer; 01b = host to controller; 10b = controller to host; 11b = reserved. Refer to the Transfer<br>Direction field in Figure 94.<br>5.<br>The Connect command is submitted and completed on the same queue that the Connect command creates. Refer<br>to section 3.3.2.2.|


**6.1** **Authentication Receive Command and Response**


The Authentication Receive command transfers the status and data result of one or more Authentication
Send commands that were previously submitted to the controller.


The association between an Authentication Receive command and previous Authentication Send
commands is dependent on the Security Protocol. The format of the data to be transferred is dependent on
the Security Protocol. Refer to SPC-5 for Security Protocol details.


Authentication Receive commands return the appropriate data corresponding to an Authentication Send
command as defined by the rules of the Security Protocol. The Authentication Receive command data shall
not be retained if there is a loss of communication between the controller and host, or if a Controller Level
Reset occurs.


**Figure 542: Authentication Receive Command – Submission Queue Entry**

|Bytes|Description|
|---|---|
|03:00|**Command Dword 0 (CDW0):**Refer to Figure 95.|
|04|**Fabrics Command Type (FCTYPE):**Set to 06h to specify an Authentication Receive command.|
|23:05|Reserved|



446


NVM Express [®] Base Specification, Revision 2.2


**Figure 542: Authentication Receive Command – Submission Queue Entry**







|Bytes|Description|
|---|---|
|39:24|**SGL Descriptor 1 (SGL1):** Refer to Figure 94.|
|40|Reserved|
|41|**SP Specific 0 (SPSP0):** The value of this field contains bits 07:00 of the Security Protocol Specific<br>field as defined in SPC-5.|
|42|**SP Specific 1 (SPSP1):** The value of this field contains bits 15:08 of the Security Protocol Specific<br>field as defined in SPC-5.|
|43|**Security Protocol (SECP):** This field specifies the security protocol as defined in SPC-5. The<br>controller shall abort the command with Invalid Parameter indicated if a reserved value of the Security<br>Protocol is specified.|
|47:44|**Allocation Length (AL):** The value of this field is specific to the Security Protocol as defined in SPC-<br>5 where INC_512 is cleared to ‘0’.|
|63:48|Reserved|


**Figure 543: Authentication Receive Response**






|Bytes|Description|
|---|---|
|07:00|Reserved|
|09:08|**SQ Head Pointer (SQHD):**Indicates the current Submission Queue Head pointer for the associated<br>Submission Queue.|
|11:10|Reserved|
|13:12|**Command Identifier (CID):**Indicates the identifier of the command that is being completed.|
|15:14|**Status Info (STS):** Indicates status for the command.<br>**Bits**<br>**Description**<br>15:01<br>**Status (STATUS):** The Status field for the command. Refer to section 4.2.3.<br>00<br>Reserved|


|Bits|Description|
|---|---|
|15:01|**Status (STATUS):** The Status field for the command. Refer to section 4.2.3.|
|00|Reserved|



**6.2** **Authentication Send Command and Response**


The Authentication Send command is used to transfer security protocol data to the controller. The data
structure transferred as part of this command contains security protocol specific commands to be performed
by the controller. The data structure may contain data or parameters associated with the security protocol
specific commands. Status and data that is to be returned to the host for the security protocol specific
commands submitted by an Authentication Send command are retrieved with the Authentication Receive
command defined in section 6.1.


The association between an Authentication Send command and subsequent Authentication Receive
commands is Security Protocol field dependent as defined in SPC-5.


**Figure 544: Authentication Send Command – Submission Queue Entry**





|Bytes|Description|
|---|---|
|03:00|**Command Dword 0 (CDW0):**Refer to Figure 95.|
|04|**Fabrics Command Type (FCTYPE):**Set to 05h to specify an Authentication Send command.|
|23:05|Reserved|
|39:24|**SGL Descriptor 1 (SGL1):** Refer to Figure 94.|
|40|Reserved|
|41|**SP Specific 0 (SPSP0):** The value of this field contains bits 07:00 of the Security Protocol Specific<br>field as defined in SPC-5.|
|42|**SP Specific 1 (SPSP1):** The value of this field contains bits 15:08 of the Security Protocol Specific<br>field as defined in SPC-5.|
|43|**Security Protocol (SECP):** This field specifies the security protocol as defined in SPC-5. The<br>controller shall abort the command with a status code of Invalid Parameter indicated if a reserved<br>value of the Security Protocol is specified.|


447


NVM Express [®] Base Specification, Revision 2.2


**Figure 544: Authentication Send Command – Submission Queue Entry**

|Bytes|Description|
|---|---|
|47:44|**Transfer Length (TL):** The value of this field is specific to the Security Protocol as defined in SPC-5<br>where INC_512 is cleared to ‘0’.|
|63:48|Reserved|



**Figure 545: Authentication Send Response**






|Bytes|Description|
|---|---|
|07:00|Reserved|
|09:08|**SQ Head Pointer (SQHD):**Indicates the current Submission Queue Head pointer for the associated<br>Submission Queue.|
|11:10|Reserved|
|13:12|**Command Identifier (CID):**Indicates the identifier of the command that is being completed.|
|15:14|**Status Info (STS):** Indicates status for the command.<br>**Bits**<br>**Description**<br>15:01<br>**Status (STATUS):**The Status field for the command. Refer to section 4.2.3.<br>00<br>Reserved|


|Bits|Description|
|---|---|
|15:01|**Status (STATUS):**The Status field for the command. Refer to section 4.2.3.|
|00|Reserved|



**6.3** **Connect Command and Response**


The Connect command is used to create a Submission and Completion Queue pair. If the Admin Queue is
specified, then the Connect command establishes an association between a host and a controller. The
fields for the submission queue entry are defined in Figure 546 and the fields for the data portion are defined
in Figure 547.


A host that uses a single Host NQN may employ multiple Host Identifiers to designate elements of the host
that access an NVM subsystem independently of each other (e.g., physical or logical partitions of the host).
Alternatively, a host may employ multiple Host NQN values to cause each element to be treated as a
separate host by an NVM subsystem.


If an NVM subsystem supports DH-HMAC-CHAP authentication (refer to section 8.3.4), then the Host NQN
and the NVM Subsystem NQN parameters in a Connect command are required to be different. If the Host
NQN and the NVM Subsystem NQN parameters in a Connect command are identical and the NVM
subsystem supports DH-HMAC-CHAP authentication, then the controller shall abort the command with a
status code of Connect Invalid Host.


The NVM subsystem shall not allocate a Controller ID in the range FFF0h to FFFFh as a valid Controller
ID on completion of a Connect command. Controller IDs FFF0h to FFFFh are defined in Figure 27. If the
host is not allowed to establish an association to any controller in the NVM subsystem, then the controller
shall abort the command with a status code of Connect Invalid Host.


If the NVM subsystem supports the dynamic controller model, then:

  - the Controller ID of FFFFh is specified as the Controller ID in a Connect command for the Admin
Queue. If the controller ID is not set to FFFFh, then the controller shall abort the command with a
status code of Connect Invalid Parameters;

  - the NVM subsystem shall allocate any available controller to the host; and

  - return that allocated Controller ID in the Connect response.


If the NVM subsystem supports the static controller model, then:

   - The host is able to request a specific controller in a Connect command for the Admin Queue. If the
host is not allowed to establish an association to the specified controller, then the controller shall
abort the command with a status code of Connect Invalid Host;

   - The Controller ID of FFFEh on the Admin Queue specifies that any Controller ID may be allocated
and returned in the Connect response; and


448


NVM Express [®] Base Specification, Revision 2.2


   - If the host specifies a Controller ID value of FFFFh for the Admin Queue, then the controller shall
abort the command with a status code of Connect Invalid Parameters.


The NVM subsystem may allocate specific controllers to particular hosts. If a host requests a controller that
is not allocated to that host, then the controller shall abort the command with a status code of Connect
Invalid Host. The mechanism for allocating specific controllers to particular hosts is outside the scope of
this specification.


The host shall establish an association with a controller and enable the controller before establishing a
connection with an I/O Queue of the controller. If the host sends a Connect command specifying a Queue
ID for an Admin Queue or I/O Queue that has already been created, then the controller shall abort the
command with a status code of Command Sequence Error.


The Controller shall abort a Connect command with a status code of Connect Invalid Parameters if:

  - the host sends a Connect command to create an I/O Queue while the controller is disabled;

  - the Host NQN, NVM Subsystem NQN, and the Controller ID values specified for an I/O Queue are
not the same as the values specified for the associated Admin Queue in which the association
between the host and controller was established;

  - the Host Identifier for an I/O Queue is not set to a value of 0h and is not set to the same value as
the value specified for the associated Admin Queue in which the association between the host and
controller was established;

  - the Host NQN or NVM Subsystem NQN values do not match the values that the NVM subsystem
is configured to support;

  - there is a syntax error in the Host NQN or NVM Subsystem NQN value (refer to section 4.7); or

  - the host specifies a Controller ID value in the range FFF0h to FFFDh.


If the NVMe Subsystem Port, NVMe Transport Type or NVMe Transport Address used by the NVMe
Transport (refer to section 6.3) are not the same as the values used for the associated Admin Queue in
which the association between the host and controller was established, then it is possible that the Connect
command is not received by an NVM subsystem. If the Connect command is received by an NVM
subsystem, then:

  - the NVM subsystem that receives the command may not be the same NVM subsystem to which
the association between the host and controller was established (i.e., the NVMe Transport Type
and NVMe Transport Address are unique to an NVM Subsystem Port); and

  - the values of the NVM Subsystem NQN or Controller ID may not be valid at that NVM Subsystem
Port (e.g., the NVM Subsystem NQN may specify a different NVM subsystem than the one that
received that Connect command, or the Controller ID may specify a controller that is already bound
to a different NVM Subsystem Port).


If this situation occurs and the Connect command is aborted, then the status code shall be set to Connect
Invalid Parameters. There is no requirement that such a Connect command be received by an NVM
subsystem (e.g., if the NVMe Transport Address is not a valid transport address, or is the address of a
fabric endpoint that does not support NVMe over Fabrics, then the resulting error, if any, is specific to the
fabric).


Submission Queue (SQ) flow control based on the SQ Head Pointer (SQHD) field in Fabrics response
capsules (refer to section 3.3.2.1.2) shall be supported by all hosts and controllers. Use of SQ flow control
is negotiated by the Connect command and response. A host requests that SQ flow control be disabled by
setting the Disable SQ Flow Control (DISSQFC) bit of the Connect Attributes field to ‘1’ in a Connect
command. A controller that agrees to disable SQ flow control shall set the SQHD field to FFFFh in the
response to that Connect command. A controller that does not agree to disable SQ flow control shall set
the SQHD field to a value other than FFFFh in the response to that Connect command.


If the Connect command did not request that SQ flow control be disabled, then the controller shall not set
the SQHD field to FFFFh in the response to that Connect command.


SQ flow control is disabled and shall not be used for a created queue pair only if:


a) the DISSQFC bit is set to ‘1’ in the Connect command that creates the queue pair; and


449


NVM Express [®] Base Specification, Revision 2.2


b) the SQHD field is set to FFFFh in the response to that Connect command.


If SQ flow control is disabled, then the SQHD field is reserved in Fabrics response capsules for all command
completions on that queue pair after the response that completes the Connect command.


SQ flow control is enabled and shall be used for a created queue pair if:


a) the DISSQFC bit is cleared to ‘0’ in the Connect command that creates the queue pair; or
b) the SQHD field is not set to FFFFh in the response to that Connect command.


If SQ flow control is enabled, then the controller shall use the SQHD field in Fabrics response capsules for
all command completions on that queue pair, except for command completions that omit the SQHD value
due to use of the SQHD pointer update optimization described in section 3.3.2.7.


**Figure 546: Connect Command – Submission Queue Entry**









|Bytes|Description|
|---|---|
|03:00|**Command Dword 0 (CDW0):**Refer to Figure 95.|
|04|**Fabrics Command Type (FCTYPE):**Set to 01h to specify a Connect command.|
|23:05|Reserved|
|39:24|**SGL Descriptor 1 (SGL1):** Refer to Figure 94.|
|41:40|**Record Format (RECFMT):**Specifies the format of the Connect command capsule. The format of the<br>record specified in this definition shall be 0h. If the NVM subsystem does not support the value specified,<br>then a status code of Incompatible Format shall be returned.|
|43:42|**Queue ID (QID):**Specifies the Queue Identifier for the Admin Queue or I/O Queue to be created. The<br>identifier is used for both the Submission and Completion Queue. The identifier for the Admin Submission<br>Queue and Admin Completion Queue is 0h. The identifier for an I/O Submission and Completion Queue is<br>in the range 1 to 65,534.<br>If the value in this field specifies the Queue ID of a queue that already exists, then the controller shall abort<br>the command with a status code of Invalid Queue Identifier.|
|45:44|**Submission Queue Size (SQSIZE):**This field indicates the size of the Submission Queue to be created.<br>If the size is 0h or larger than the controller supports, then a status code of Connect Invalid Parameters<br>shall be returned. The maximum size of the Admin Submission Queue is specified in the Discovery Log<br>Page Entry for the NVM subsystem. Refer to Figure 295. This is a 0’s based value.|
|46|**Connect Attributes (CATTR):**This field indicates attributes for the connection.<br>**Bits**<br>**Description**<br>7:5<br>Reserved<br>4 <br>**Connecting Entity (CONNENT):** Indicates the type of entity performing the Connect<br>command. If this bit is set to ‘1’, then the entity performing the Connect command is a<br>Discovery controller. If this bit is cleared to ‘0’, then the entity performing the Connect<br>command is a host.<br>3 <br>**Individual I/O Queue Deletion Support (INDIVIOQDELS):** Indicates support for deleting<br>individual I/O Queues. If this bit is set to ‘1’, then the host supports the deletion of individual<br>I/O Queues. If this bit is cleared to ‘0’, then the host does not support the deletion of<br>individual I/O Queues.<br>2 <br>**Disable SQ Flow Control (DISSQFC):** If this bit is set to ‘1’, then the host is requesting<br>that SQ flow control be disabled. If this bit is cleared to ‘0’, then SQ flow control shall not<br>be disabled.<br>1:0<br>**Priority Class (PRIOCLASS):**Indicates the priority class to use for commands within this<br>Submission Queue. This field is only used when the weighted round robin with urgent<br>priority class is the arbitration mechanism selected (refer to CC.AMS in Figure 41, the field<br>is ignored if weighted round robin with urgent priority class is not used. Refer to section<br>3.4.4. This field is only valid for I/O Queues and shall be cleared to 00b for Admin Queue<br>connections.<br>**Value**<br>**Definition**<br>00b<br>Urgent<br>01b<br>High<br>10b<br>Medium<br>11b<br>Low|


|Bits|Description|
|---|---|
|7:5|Reserved|
|4|**Connecting Entity (CONNENT):** Indicates the type of entity performing the Connect<br>command. If this bit is set to ‘1’, then the entity performing the Connect command is a<br>Discovery controller. If this bit is cleared to ‘0’, then the entity performing the Connect<br>command is a host.|
|3|**Individual I/O Queue Deletion Support (INDIVIOQDELS):** Indicates support for deleting<br>individual I/O Queues. If this bit is set to ‘1’, then the host supports the deletion of individual<br>I/O Queues. If this bit is cleared to ‘0’, then the host does not support the deletion of<br>individual I/O Queues.|
|2|**Disable SQ Flow Control (DISSQFC):** If this bit is set to ‘1’, then the host is requesting<br>that SQ flow control be disabled. If this bit is cleared to ‘0’, then SQ flow control shall not<br>be disabled.|
|1:0|**Priority Class (PRIOCLASS):**Indicates the priority class to use for commands within this<br>Submission Queue. This field is only used when the weighted round robin with urgent<br>priority class is the arbitration mechanism selected (refer to CC.AMS in Figure 41, the field<br>is ignored if weighted round robin with urgent priority class is not used. Refer to section<br>3.4.4. This field is only valid for I/O Queues and shall be cleared to 00b for Admin Queue<br>connections.<br>**Value**<br>**Definition**<br>00b<br>Urgent<br>01b<br>High<br>10b<br>Medium<br>11b<br>Low|


|Value|Definition|
|---|---|
|00b|Urgent|
|01b|High|
|10b|Medium|
|11b|Low|


450


NVM Express [®] Base Specification, Revision 2.2


**Figure 546: Connect Command – Submission Queue Entry**







|Bytes|Description|
|---|---|
|47|Reserved|
|51:48|**Keep Alive Timeout (KATO):**In the Connect command for the Admin Queue, this field has the same<br>definition as the Keep Alive Timeout (KATO) field of the Keep Alive Timer feature (refer to section<br>5.1.25.1.8). Upon successful completion of the Connect command, the controller shall set the KATO field<br>in the Keep Alive Timer feature. Refer to section 3.9.2 for a description of activating the Keep Alive Timer.<br>In the Connect command for an I/O Queue, this field is reserved.|
|53:52|**NVM Set Identifier (NVMSETID):** This field indicates the identifier of the NVM Set to be associated with<br>this Submission Queue. This field is only valid for I/O Queues.<br>In the Connect command for an Admin Queue, the:<br>• <br>host should clear this field to 0h;<br>• <br>controller shall ignore this field; and<br>• <br>Submission Queue is not associated with any NVM Set.<br>In the Connect command for an I/O queue, if the SQ Associations capability is not supported (refer to<br>section 8.1.25) or this field is cleared to 0h, then this Submission Queue is not associated with any specific<br>NVM Set.<br>If the SQ Associations capability is supported (refer to section 8.1.25) and this field contains a non-zero<br>value that is not indicated in the NVM Set List (refer to Figure 318), then the controller shall abort the<br>command with a status code of Invalid Field in Command.<br>The host should not submit commands for namespaces associated with other NVM Sets in this Submission<br>Queue (refer to section 8.1.25).|
|63:54|Reserved|


**Figure 547: Connect Command – Data**









|Bytes|Description|
|---|---|
|15:00|**Host Identifier (HOSTID):** This field has the same definition as the Host Identifier defined in<br>section 5.1.25.1.28.<br>For a Connect command to create an Admin Queue (i.e., the QID field is cleared to 0h) that<br>completes successfully the controller shall set the current Host Identifier (refer to section<br>5.1.25.1.28.2) to this value.<br>For a Connect command to create an I/O queue (i.e., the QID field is set to a non-zero value):<br>• <br>if this field is cleared to 0h, then the controller shall ignore this field; and<br>• <br>if this field is set to a non-zero value and the value in this field does not match the value<br>in the Host Identifier feature, then the controller shall abort the command with a status<br>code of Connect Invalid Parameters.|
|17:16|**Controller ID (CNTLID):**Specifies the controller ID requested. This field corresponds to the<br>Controller ID (CNTLID) value returned in the Identify Controller data structure for a particular<br>controller. If the NVM subsystem uses the dynamic controller model, then the value shall be<br>FFFFh for the Admin Queue and any available controller may be returned. If the NVM subsystem<br>uses the static controller model and the value is FFFEh for the Admin Queue, then any available<br>controller may be returned.|
|255:18|Reserved|
|511:256|**NVM Subsystem NVMe Qualified Name (SUBNQN):**NVMe Qualified Name (NQN) that<br>uniquely identifies the NVM subsystem. Refer to section 4.7.|
|767:512|**Host NVMe Qualified Name (HOSTNQN):**NVMe Qualified Name (NQN) that uniquely<br>identifies the host. Refer to section 4.7.|
|1023:768|Reserved|


The Connect response provides status for the Connect command. If a connection is established, then the
Controller ID allocated to the host is returned. The Connect response is defined in Figure 548.


451


NVM Express [®] Base Specification, Revision 2.2


For a Connect command that fails, the controller shall not:

  - return a status code of Invalid Field in Command; and

  - add an entry to the Error Information log page (refer to section 5.1.12.1.2).


**Figure 548: Connect Response**





|Bytes|Description|
|---|---|
|03:00|**Status Code Specific (SCS):**The value is dependent on the status returned. Refer to Figure 549.|
|07:04|Reserved|
|09:08|**SQ Head Pointer (SQHD):**If the Connect command requested that SQ flow control be disabled, then a<br>value of FFFFh in this field indicates that SQ flow control is disabled for the created queue pair.<br>Otherwise, this field indicates the current Submission Queue Head pointer for the associated<br>Submission Queue and also indicates that SQ flow control is enabled for the created queue pair.|
|11:10|Reserved|
|13:12|**Command Identifier (CID):**Indicates the identifier of the command that is being completed.|
|15:14|**Status Info (STS):** Indicates status for the command.<br>**Bits**<br>**Description**<br>15:01<br>**Status (STATUS):** The Status field for the command. Refer to section 4.2.3. Refer<br>to Figure 105 for values specific to the Connect command.<br>00<br>Reserved|


|Bits|Description|
|---|---|
|15:01|**Status (STATUS):** The Status field for the command. Refer to section 4.2.3. Refer<br>to Figure 105 for values specific to the Connect command.|
|00|Reserved|


**Figure 549: Connect Response – Dword 0 Value Based on Status Code**















|Status Code|Definition of Dword 0|
|---|---|
|Successful<br>Completion|**Bytes**<br>**Description**<br>01:00<br>**Controller ID (CNTLID):**Specifies the controller ID allocated to the host. If a<br>particular controller was specified in the CNTLID field of the Connect command,<br>then this field shall contain the same value.<br>03:02<br>**Authentication and Security Requirements (AUTHREQ):**Specifies the NVMe<br>in-band authentication and security requirements. The field is bit significant. If all<br>bits are cleared to ‘0’, then no requirements are specified.<br>**Bits**<br>**Description**<br>15:03<br>Reserved<br>02<br>**Authentication and Secure Channel Required (ASCR):**If this<br>bit is set to ‘1’, then authentication using NVMe over Fabrics<br>Authentication<br>protocols<br>followed<br>by<br>secure<br>channel<br>establishment is required and the ATR bit should be cleared to<br>‘0’. If this bit is cleared to ‘0’, then authentication using NVMe over<br>Fabrics Authentication protocols followed by secure channel<br>establishment is not required.<br>01<br>**Authentication Transaction Required (ATR):**If this bit is set to<br>‘1’, then authentication using NVMe over Fabrics Authentication<br>protocols is required. If this bit is cleared to ‘0’, then authentication<br>using NVMe over Fabrics Authentication protocols is not required.<br>00<br>Obsolete.<br>|


|Bytes|Description|
|---|---|
|01:00|**Controller ID (CNTLID):**Specifies the controller ID allocated to the host. If a<br>particular controller was specified in the CNTLID field of the Connect command,<br>then this field shall contain the same value.|
|03:02|**Authentication and Security Requirements (AUTHREQ):**Specifies the NVMe<br>in-band authentication and security requirements. The field is bit significant. If all<br>bits are cleared to ‘0’, then no requirements are specified.<br>**Bits**<br>**Description**<br>15:03<br>Reserved<br>02<br>**Authentication and Secure Channel Required (ASCR):**If this<br>bit is set to ‘1’, then authentication using NVMe over Fabrics<br>Authentication<br>protocols<br>followed<br>by<br>secure<br>channel<br>establishment is required and the ATR bit should be cleared to<br>‘0’. If this bit is cleared to ‘0’, then authentication using NVMe over<br>Fabrics Authentication protocols followed by secure channel<br>establishment is not required.<br>01<br>**Authentication Transaction Required (ATR):**If this bit is set to<br>‘1’, then authentication using NVMe over Fabrics Authentication<br>protocols is required. If this bit is cleared to ‘0’, then authentication<br>using NVMe over Fabrics Authentication protocols is not required.<br>00<br>Obsolete.|


|Bits|Description|
|---|---|
|15:03|Reserved|
|02|**Authentication and Secure Channel Required (ASCR):**If this<br>bit is set to ‘1’, then authentication using NVMe over Fabrics<br>Authentication<br>protocols<br>followed<br>by<br>secure<br>channel<br>establishment is required and the ATR bit should be cleared to<br>‘0’. If this bit is cleared to ‘0’, then authentication using NVMe over<br>Fabrics Authentication protocols followed by secure channel<br>establishment is not required.|
|01|**Authentication Transaction Required (ATR):**If this bit is set to<br>‘1’, then authentication using NVMe over Fabrics Authentication<br>protocols is required. If this bit is cleared to ‘0’, then authentication<br>using NVMe over Fabrics Authentication protocols is not required.|
|00|Obsolete.|


452


NVM Express [®] Base Specification, Revision 2.2


**Figure 549: Connect Response – Dword 0 Value Based on Status Code**








|Bits|Description|
|---|---|
|7:1|Reserved|
|0|**Invalid Parameter Start (IPS):** If this bit is cleared to ‘0’, then the<br>invalid parameter is specified from the start of the SQE. If this bit is<br>set to ‘1’, then the invalid parameter is specified from the start of the<br>data.|










|Status Code|Definition of Dword 0|Col3|Col4|Col5|
|---|---|---|---|---|
|Connect<br>Invalid<br>Parameters||**Bytes**|**Description**||
|Connect<br>Invalid<br>Parameters||01:00|**Invalid Parameter Offset (IPO):**If an invalid parameter is reported, then this<br>field specifies the offset in bytes to the invalid parameter from the start of the<br>SQE or the data.|**Invalid Parameter Offset (IPO):**If an invalid parameter is reported, then this<br>field specifies the offset in bytes to the invalid parameter from the start of the<br>SQE or the data.|
|Connect<br>Invalid<br>Parameters||02|**Invalid Attributes (IATTR):**Specifies attributes of the invalid field parameter.<br>**Bits**<br>**Description**<br>7:1<br>Reserved<br>0 <br>**Invalid Parameter Start (IPS):** If this bit is cleared to ‘0’, then the<br>invalid parameter is specified from the start of the SQE. If this bit is<br>set to ‘1’, then the invalid parameter is specified from the start of the<br>data.|**Invalid Attributes (IATTR):**Specifies attributes of the invalid field parameter.<br>**Bits**<br>**Description**<br>7:1<br>Reserved<br>0 <br>**Invalid Parameter Start (IPS):** If this bit is cleared to ‘0’, then the<br>invalid parameter is specified from the start of the SQE. If this bit is<br>set to ‘1’, then the invalid parameter is specified from the start of the<br>data.|
|Connect<br>Invalid<br>Parameters||03|Reserved|Reserved|
|All Other<br>Status Values||**Bytes**|**Description**||
|All Other<br>Status Values||03:00|Reserved|Reserved|



**6.4** **Disconnect Command and Response**


The Disconnect command is used to delete the I/O Queue on which the command is submitted. If a
Disconnect command is submitted on an Admin Queue, then the controller shall abort the command with a
status code of Invalid Queue Type. If the controller is not able to delete the I/O Queue, then the controller
shall abort the command with a status code of Controller Busy. The fields for the submission queue entry
are defined in Figure 550.


The NVMe Transport connection is not deleted upon issuance of a Disconnect command; the host and
controller may delete the NVMe Transport connection and associated resources after all NVMe Queues
(I/O Queues and/or Admin Queue) associated with that NVMe Transport connection have been deleted
(refer to section 3.3.2.4).


The completion queue entry for the Disconnect command shall be the last entry submitted to the I/O Queue
Completion queue by the controller (i.e., no completion queue entries shall be submitted to the I/O Queue
Completion Queue after the completion queue entry for the Disconnect command). The controller shall
ensure that no further command processing is performed for any command on an I/O queue after sending
the completion queue entry for the Disconnect command.


The host should not submit commands to an I/O Submission Queue after the submission of a Disconnect
command to that I/O Submission Queue; submitting commands to an I/O Queue after a Disconnect
command is submitted to that I/O Queue results in undefined behavior.


**Figure 550: Disconnect Command – Submission Queue Entry**

|Bytes|Description|
|---|---|
|03:00|**Command Dword 0 (CDW0):**Refer to Figure 95. Byte 01 is cleared to 0h.|
|04|**Fabrics Command Type (FCTYPE):**Set to 08h to specify a Disconnect command.|
|39:05|Reserved|
|41:40|**Record Format (RECFMT):** Specifies the format of the Disconnect command capsule. The format of<br>the record specified in this definition shall be 0h. If the NVM subsystem does not support the value<br>specified, then a status code of Incompatible Format shall be returned.|
|63:42|Reserved|



The Disconnect response provides status for the Disconnect command. The Disconnect response is
defined in Figure 551.


453


NVM Express [®] Base Specification, Revision 2.2


**Figure 551: Disconnect Response**






|Bytes|Description|
|---|---|
|07:00|Reserved|
|09:08|**SQ Head Pointer (SQHD):**Indicates the current Submission Queue Head pointer for the associated<br>Submission Queue.|
|11:10|Reserved|
|13:12|**Command Identifier (CID):**Indicates the identifier of the command that is being completed.|
|15:14|**Status Info (STS):** Indicates status for the command.<br>**Bits**<br>**Description**<br>15:01<br>**Status (STATUS):**The Status field for the command. Refer to section 4.2.2.<br>Refer to Figure 105 for values specific to the Disconnect command.<br>00<br>Reserved|


|Bits|Description|
|---|---|
|15:01|**Status (STATUS):**The Status field for the command. Refer to section 4.2.2.<br>Refer to Figure 105 for values specific to the Disconnect command.|
|00|Reserved|



**6.5** **Property Get Command and Response**


The Property Get command is used to specify the property value to return to the host (refer to section 3.1.4).
The fields for the Property Get command are defined in Figure 552. If an invalid property or invalid offset is
specified, then a status code of Invalid Field in Command shall be returned.


**Figure 552: Property Get Command – Submission Queue Entry**







|Bytes|Description|
|---|---|
|03:00|**Command Dword 0 (CDW0):**Refer to Figure 95. Byte 01 is cleared to 0h.|
|04|**Fabrics Command Type (FCTYPE):**Set to 04h to specify a Property Get command.|
|39:05|Reserved|
|40|**Attributes (ATTRIB):**Specifies attributes for the Property Get command.<br>**Bits**<br>**Description**<br>7:3<br>Reserved<br>2:0<br>**Property Return Size (PRS):** This field specifies the size of the property to return. Valid<br>values are shown in the table below.<br>**Value**<br>**Definition**<br>000b<br>4 bytes<br>001b<br>8 bytes<br>010b to 111b<br>Reserved|
|43:41|Reserved|
|47:44|**Offset (OFST):**Specifies the offset to the property to get. Refer to section 3.1.4.|
|63:48|Reserved|


|Bits|Description|
|---|---|
|7:3|Reserved|
|2:0|**Property Return Size (PRS):** This field specifies the size of the property to return. Valid<br>values are shown in the table below.<br>**Value**<br>**Definition**<br>000b<br>4 bytes<br>001b<br>8 bytes<br>010b to 111b<br>Reserved|


|Value|Definition|
|---|---|
|000b|4 bytes|
|001b|8 bytes|
|010b to 111b|Reserved|


The Property Get response is used to return the value of the property requested to the host. The Property
Get response is defined in Figure 553.


**Figure 553: Property Get Response**











|Bytes|Description|
|---|---|
|07:00|**Value (VALUE):**Indicates the value returned for the property if the Property Get command is<br>successful. If the size of the property is four bytes, then the value is specified in bytes 03:00 and bytes<br>07:04 are reserved.|
|09:08|**SQ Head Pointer (SQHD):**Indicates the current Submission Queue Head pointer for the associated<br>Submission Queue.|
|11:10|Reserved|
|13:12|**Command Identifier (CID):**Indicates the identifier of the command that is being completed.|
|15:14|**Status Info (STS):** Indicates status for the command.<br>**Bits**<br>**Description**<br>15:01<br>**Status (STATUS):** The Status field for the command. Refer to section 4.2.2.<br>00<br>Reserved|


|Bits|Description|
|---|---|
|15:01|**Status (STATUS):** The Status field for the command. Refer to section 4.2.2.|
|00|Reserved|


454


NVM Express [®] Base Specification, Revision 2.2


**6.6** **Property Set Command and Response**


The Property Set command is used to set the value of a property (refer to section 3.1.4). The fields for the
Property Set command are defined in Figure 554. If an invalid property or invalid offset is specified, then a
status code of Invalid Field in Command shall be returned.


**Figure 554: Property Set Command – Submission Queue Entry**








|Bits|Description|
|---|---|
|7:3|Reserved|
|2:0|**Property Update Size (PUS):** This field specifies the size of the property to update. Valid<br>values are shown in the table below.<br>**Value**<br>**Definition**<br>000b<br>4 bytes<br>001b<br>8 bytes<br>010b to 111b<br>Reserved|


|Value|Definition|
|---|---|
|000b|4 bytes|
|001b|8 bytes|
|010b to 111b|Reserved|


|Bytes|Description|
|---|---|
|03:00|**Command Dword 0 (CDW0):**Refer to Figure 95. Byte 01 is cleared to 0h.|
|04|**Fabrics Command Type (FCTYPE):**Cleared to 00h to specify a Property Set command.|
|39:05|Reserved|
|40|**Attributes (ATTRIB):**Specifies attributes for the Property Set command.<br>**Bits**<br>**Description**<br>7:3<br>Reserved<br>2:0<br>**Property Update Size (PUS):** This field specifies the size of the property to update. Valid<br>values are shown in the table below.<br>**Value**<br>**Definition**<br>000b<br>4 bytes<br>001b<br>8 bytes<br>010b to 111b<br>Reserved|
|43:41|Reserved|
|47:44|**Offset (OFST):**Specifies the offset to the property to set. Refer to section 3.1.4.|
|55:48|**Value (VALUE):**Specifies the value used to update the property. If the size of the property is four<br>bytes, then the value is specified in bytes 51:48 and bytes 55:52 are reserved.|
|63:56|Reserved|



The Property Set response provides status for the Property Set command. The Property Set response is
defined in Figure 555.


**Figure 555: Property Set Response**





|Bytes|Description|
|---|---|
|07:00|Reserved|
|09:08|**SQ Head Pointer (SQHD):**Indicates the current Submission Queue Head pointer for the associated<br>Submission Queue.|
|11:10|Reserved|
|13:12|**Command Identifier (CID):**Indicates the identifier of the command that is being completed.|
|15:14|**Status Info (STS):** Indicates status for the command.<br>**Bits**<br>**Description**<br>15:01<br>**Status (STATUS):**Status field for the command. Refer to section 4.2.2.<br>00<br>Reserved|


|Bits|Description|
|---|---|
|15:01|**Status (STATUS):**Status field for the command. Refer to section 4.2.2.|
|00|Reserved|


455


