NVM Express [®] Base Specification, Revision 2.2


**4 Data Structures**


This section describes data structures used by the NVM Express Interface.


**4.1** **Submission Queue Entry**


**Admin Command and I/O Command Common SQE**


Each Common Command Format command is 64 bytes in size.


Command Dword 0, Namespace Identifier, Metadata Pointer, PRP Entry 1, PRP Entry 2, SGL Entry 1, and
Metadata SGL Segment Pointer have common definitions for all Admin commands and I/O commands for
all I/O Command Sets. Metadata Pointer, PRP Entry 1, PRP Entry 2, and Metadata SGL Segment Pointer
are not used by all commands. Command Dword 0 is defined in Figure 91.


**Figure 91: Command Dword 0**












|Value|Definition|
|---|---|
|00b|**PRPS Used:** PRPs are used for this transfer.|
|01b|**SGLs Used MPTR Address:** SGLs are used for this transfer. If used, Metadata Pointer<br>(MPTR) contains an address of a single contiguous physical buffer.<br>Refer to the Metadata Buffer Alignment (MBA) bit of the SGLS field in the Identify<br>Controller data structure (refer to Figure 313) for alignment requirements.|
|10b|**SGLs Used MPTR SGL Segment:** SGLs are used for this transfer. If used, Metadata<br>Pointer (MPTR) contains an address of an SGL segment containing exactly one SGL<br>Descriptor that is qword aligned.|
|11b|Reserved|





|Bits|Description|
|---|---|
|31:16|**Command Identifier (CID):**This field specifies a unique identifier for the command when combined with the<br>Submission Queue identifier.<br>The value of FFFFh should not be used as the Error Information log page (refer to section 5.1.12.1.2) uses<br>this value to indicate an error is not associated with a particular command.|
|15:14|**PRP or SGL for Data Transfer (PSDT):** This field specifies whether PRPs or SGLs are used for any data<br>transfer associated with the command. PRPs shall be used for all Admin commands for NVMe over PCIe<br>implementations. SGLs shall be used for all Admin and I/O commands for NVMe over Fabrics implementations<br>(i.e., this field set to 01b). An NVMe Transport may support only specific values (refer to the applicable NVMe<br>Transport binding specification for details).<br>**Value**<br>**Definition**<br>00b<br>**PRPS Used:** PRPs are used for this transfer.<br>01b<br>**SGLs Used MPTR Address:** SGLs are used for this transfer. If used, Metadata Pointer<br>(MPTR) contains an address of a single contiguous physical buffer.<br>Refer to the Metadata Buffer Alignment (MBA) bit of the SGLS field in the Identify<br>Controller data structure (refer to Figure 313) for alignment requirements.<br>10b<br>**SGLs Used MPTR SGL Segment:** SGLs are used for this transfer. If used, Metadata<br>Pointer (MPTR) contains an address of an SGL segment containing exactly one SGL<br>Descriptor that is qword aligned.<br>11b<br>Reserved<br>If there is metadata that is not interleaved with the user data, as specified in the Format NVM command, then<br>the Metadata Pointer (MPTR) field is used to point to the metadata. The definition of the Metadata Pointer field<br>is dependent on the setting in this field. Refer to Figure 92.|
|13:10|Reserved|
|09:08|**Fused Operation (FUSE):**In a fused operation, a complex command is created by “fusing” together two<br>simpler commands. Refer to section 3.4.2. This field specifies whether this command is part of a fused<br>operation and if so, which command it is in the sequence.<br>**Value**<br>**Definition**<br>00b<br>Normal operation<br>01b<br>First command of Fused operation<br>10b<br>Second command of Fused operation<br>11b<br>Reserved|


|Value|Definition|
|---|---|
|00b|Normal operation|
|01b|First command of Fused operation|
|10b|Second command of Fused operation|
|11b|Reserved|


131


NVM Express [®] Base Specification, Revision 2.2


**Figure 91: Command Dword 0**








|Bits|Description|
|---|---|
|07:00|**Opcode (OPC):**This field specifies the opcode of the command to be executed as shown here:<br>**Bits**<br>**Description**<br>07:02<br>**Function (FN):**This field contains a value that, in combination with the other fields in the<br>Opcode data structure, creates a unique combined opcode value.<br>01:00<br>**Data Transfer Direction (DTD):** This field indicates the direction of a data transfer, if any.All<br>options of the command shall transfer data as specified or transfer no data. All<br>commands, including vendor specific commands, shall follow this convention. <br>**Value**<br>**Definition**<br>00b<br>**No Data Transfer:**No data is transferred.<br>01b<br>**Host to Controller Transfer:** Data is transferred from the host to the<br>controller.<br>10b<br>**Controller to Host Transfer:** Data is transferred from the controller to the<br>host.<br>11b<br>**Bi-Directional Transfer:** Data is transferred from the host to the controller<br>and from the controller to the host.|


|Bits|Description|
|---|---|
|07:02|**Function (FN):**This field contains a value that, in combination with the other fields in the<br>Opcode data structure, creates a unique combined opcode value.|
|01:00|**Data Transfer Direction (DTD):** This field indicates the direction of a data transfer, if any.All<br>options of the command shall transfer data as specified or transfer no data. All<br>commands, including vendor specific commands, shall follow this convention. <br>**Value**<br>**Definition**<br>00b<br>**No Data Transfer:**No data is transferred.<br>01b<br>**Host to Controller Transfer:** Data is transferred from the host to the<br>controller.<br>10b<br>**Controller to Host Transfer:** Data is transferred from the controller to the<br>host.<br>11b<br>**Bi-Directional Transfer:** Data is transferred from the host to the controller<br>and from the controller to the host.|


|Value|Definition|
|---|---|
|00b|**No Data Transfer:**No data is transferred.|
|01b|**Host to Controller Transfer:** Data is transferred from the host to the<br>controller.|
|10b|**Controller to Host Transfer:** Data is transferred from the controller to the<br>host.|
|11b|**Bi-Directional Transfer:** Data is transferred from the host to the controller<br>and from the controller to the host.|



The Common Command Format is defined in Figure 92. Any additional I/O Command Set defined in the
future may use an alternate command size or format.


SGLs shall not be used for Admin commands in NVMe over PCIe implementations.


**Figure 92: Common Command Format**







|Bytes|Description|
|---|---|
|03:00|**Command Dword 0 (CDW0):**This field is common to all commands and is defined in Figure 91.|
|07:04|**Namespace Identifier (NSID):**This field specifies the namespace that this command applies to. If the<br>namespace identifier is not used for the command, then this field shall be cleared to 0h. The value FFFFFFFFh<br>in this field is a broadcast value (refer to section 3.2.1.2), where the scope (e.g., the NVM subsystem, all<br>attached namespaces, or all namespaces in the NVM subsystem) is dependent on the command. Refer to<br>Figure 142 and Figure 556 for commands that support the use of the value FFFFFFFFh in this field.<br>Specifying an inactive namespace identifier (refer to section 3.2.1.4) in a command that uses the namespace<br>identifier shall cause the controller to abort the command with a status code of Invalid Field in Command,<br>unless otherwise specified. Specifying an invalid namespace identifier (refer to section 3.2.1.2) in a command<br>that uses the namespace identifier shall cause the controller to abort the command with a status code of Invalid<br>Namespace or Format, unless otherwise specified.<br>If the namespace identifier is used for the command (refer to Figure 142), the value FFFFFFFFh is not<br>supported for that command, and the host specifies a value of FFFFFFFFh, then the controller shall abort the<br>command with a status code of Invalid Field in Command, unless otherwise specified.<br>If the namespace identifier is not used for the command and the host specifies a value from 1h to FFFFFFFFh,<br>then the controller shall abort the command with a status code of Invalid Field in Command, unless otherwise<br>specified.|
|11:08|**Command Dword 2 (CDW2):** This field is command specific Dword2.|
|15:12|**Command Dword 3 (CDW3):**This field is command specific Dword3.|


132


NVM Express [®] Base Specification, Revision 2.2


**Figure 92: Common Command Format**





|Bytes|Description|
|---|---|
|23:16|**Metadata Pointer (MPTR):**If CDW0.PSDT (refer to Figure 91) is cleared to 00b, then this field shall contain<br>the address of a contiguous physical buffer of metadata and that address shall be dword aligned (i.e., bits 1:0<br>cleared to 00b). The controller is not required to check that bits 1:0 are cleared to 00b. The controller may<br>report an error of Invalid Field in Command if bits 1:0 are not cleared to 00b. If the controller does not report<br>an error of Invalid Field in Command, then the controller shall operate as if bits 1:0 are cleared to 00b.<br>If CDW0.PSDT is set to 01b, then this field shall contain the address of a contiguous physical buffer of<br>metadata. Refer to the Metadata Buffer Alignment (MBA) bit of the SGLS field in the Identify Controller data<br>structure for alignment requirements.<br>If CDW0.PSDT is set to 10b, then this field shall contain the address of an SGL segment that contains exactly<br>one SGL Descriptor. The address of that SGL segment shall be qword aligned (i.e., bits 2:0 cleared to 000b).<br>The SGL Descriptor contained in that SGL segment is the first SGL Descriptor of the metadata for the<br>command. If the SGL Descriptor contained in that SGL segment is an SGL Data Block descriptor, then that<br>SGL Data Block Descriptor is the only SGL Descriptor and therefore describes the entire metadata data<br>transfer. Refer to section 4.3.2. The controller is not required to check that bits 2:0 are cleared to 000b. The<br>controller may report an error of Invalid Field in Command if bits 2:0 are not cleared to 000b. If the controller<br>does not report an error of Invalid Field in Command, then the controller shall operate as if bits 2:0 are cleared<br>to 000b.|


133


NVM Express [®] Base Specification, Revision 2.2


**Figure 92: Common Command Format**








|39:32|PRP Entry 2 (PRP2): This field:<br>• is reserved if the data transfer does not cross a memory page boundary;<br>• specifies the Page Base Address of the second memory page if the data<br>transfer crosses exactly one memory page boundary. E.g.,:<br>o the command data transfer length is equal in size to one memory<br>page and the offset portion of the PBAO field of PRP1 is non-<br>zero; or<br>o the Offset portion of the PBAO field of PRP1 is equal to 0h and<br>the command data transfer length is greater than one memory<br>page and less than or equal to two memory pages in size;<br>and<br>• is a PRP List pointer if the data transfer crosses more than one memory<br>page boundary. E.g.,:<br>o the command data transfer length is greater than or equal to two<br>memory pages in size but the offset portion of the PBAO field of<br>PRP1 is non-zero; or<br>o the command data transfer length is equal in size to more than<br>two memory pages and the Offset portion of the PBAO field of<br>PRP1 is equal to 0h.|
|---|---|
|31:24|**PRP Entry 1 (PRP1):**This field contains:<br>• <br>the first PRP entry for the command; or<br>• <br>a PRP List pointer,<br>depending on the command (e.g., the Create I/O Completion Queue command<br>(refer to Figure 474)).|









|Bytes|Description|
|---|---|
|39:24|**Data Pointer (DPTR):**This field specifies the data used in the command.<br>If CDW0.PSDT is cleared to 00b, then the definition of this field is:<br>39:32<br>**PRP Entry 2 (PRP2):**This field:<br>• <br>is reserved if the data transfer does not cross a memory page boundary;<br>• <br>specifies the Page Base Address of the second memory page if the data<br>transfer crosses exactly one memory page boundary. E.g.,:<br>`o` <br>the command data transfer length is equal in size to one memory<br>page and the offset portion of the PBAO field of PRP1 is non-<br>zero; or<br>`o` <br>the Offset portion of the PBAO field of PRP1 is equal to 0h and<br>the command data transfer length is greater than one memory<br>page and less than or equal to two memory pages in size;<br>and<br>• <br>is a PRP List pointer if the data transfer crosses more than one memory<br>page boundary. E.g.,:<br>`o` <br>the command data transfer length is greater than or equal to two<br>memory pages in size but the offset portion of the PBAO field of<br>PRP1 is non-zero; or <br>`o` <br>the command data transfer length is equal in size to more than<br>two memory pages and the Offset portion of the PBAO field of<br>PRP1 is equal to 0h. <br>31:24<br>**PRP Entry 1 (PRP1):**This field contains:<br>• <br>the first PRP entry for the command; or<br>• <br>a PRP List pointer,<br>depending on the command (e.g., the Create I/O Completion Queue command<br>(refer to Figure 474)).<br>If CDW0.PSDT is set to 01b or 10b, then the definition of this field is:<br>39:24<br>**SGL Entry 1 (SGL1):**This field contains the first SGL segment for the command.<br>If the SGL segment is an SGL Data Block or Keyed SGL Data Block or Transport<br>SGL Data Block descriptor, then it describes the entire data transfer. If more than<br>one SGL segment is needed to describe the data transfer, then the first SGL<br>segment is a Segment, or Last Segment descriptor. Refer to section 4.3.2 for the<br>definition of SGL segments and descriptor types.<br>The NVMe Transport may support a subset of SGL Descriptor types and features<br>as defined in the NVMe Transport binding specification.|
|43:40|**Command Dword 10 (CDW10):** This field is command specific Dword 10.|
|47:44|**Command Dword 11 (CDW11):** This field is command specific Dword 11.|
|51:48|**Command Dword 12 (CDW12):** This field is command specific Dword 12.|
|55:52|**Command Dword 13 (CDW13):** This field is command specific Dword 13.|
|59:56|**Command Dword 14 (CDW14):** This field is command specific Dword 14.|
|63:60|**Command Dword 15 (CDW15):** This field is command specific Dword 15.|


In addition to the fields commonly defined for the Common Command Format, Vendor Specific commands
may support the Number of Dwords in Data Transfer and Number of Dwords in Metadata Transfer fields. If
supported, the command format for the Vendor Specific commands are defined in Figure 93. For more
details, refer to section 8.1.26.


134


NVM Express [®] Base Specification, Revision 2.2


**Figure 93: Common Command Format – Vendor Specific Commands (Optional)**









|Bytes|Description|
|---|---|
|03:00|**Command Dword 0 (CDW0):**This field is common to all commands and is defined in Figure 91.|
|07:04|**Namespace Identifier (NSID):**This field indicates the namespace ID that this command applies to.<br>If the namespace ID is not used for the command, then this field shall be cleared to 0h. Setting this<br>value to FFFFFFFFh causes the command to be applied to all namespaces attached to the controller<br>processing the command, unless otherwise specified.<br>The behavior of a controller in response to an inactive namespace ID for a vendor specific command<br>is vendor specific. Specifying an invalid namespace ID in a command that uses the namespace ID<br>shall cause the controller to abort the command with a status code of Invalid Namespace or Format,<br>unless otherwise specified.|
|15:08|Reserved|
|39:16|**Meatadata and Data Pointers (MDPTR):** Refer to Figure 92 for the definition of these fields.|
|43:40|**Number of Dwords in Data Transfer (NDT):** This field indicates the number of dwords in the data<br>transfer.|
|47:44|**Number of Dwords in Metadata Transfer (NDM):** This field indicates the number of dwords in the<br>metadata transfer.|
|51:48|**Command Dword 12 (CDW12):** This field is command specific Dword 12.|
|55:52|**Command Dword 13 (CDW13):** This field is command specific Dword 13.|
|59:56|**Command Dword 14 (CDW14):** This field is command specific Dword 14.|
|63:60|**Command Dword 15 (CDW15):** This field is command specific Dword 15.|


**Fabrics Command Common SQE**


The common submission queue entry for Fabrics commands is shown in Figure 94.


**Figure 94: Fabrics Command – Submission Queue Entry Format**










|Bits|Description|
|---|---|
|07:02|**Function (FN):**This field contains a value that, in combination with the other fields in<br>the Fabrics Command Type data structure, creates a unique Combined Fabrics<br>Command Type.|
|01:00|**Data Transfer Direction (DTD):** This field indicates the direction of a data transfer, if<br>any.All options of the command shall transfer data as specified or transfer no<br>data. All commands, including vendor specific commands, shall follow this<br>convention. <br>**Value**<br>**Definition**<br>00b<br>**No Data Transfer:**No data is transferred.<br>01b<br>**Host to Controller Transfer:** Data is transferred from the host to the<br>controller.<br>10b<br>**Controller to Host Transfer:** Data is transferred from the controller to the<br>host.<br>11b<br>Reserved|


|Value|Definition|
|---|---|
|00b|**No Data Transfer:**No data is transferred.|
|01b|**Host to Controller Transfer:** Data is transferred from the host to the<br>controller.|
|10b|**Controller to Host Transfer:** Data is transferred from the controller to the<br>host.|
|11b|Reserved|







|Bytes|Description|
|---|---|
|03:00|**Command Dword 0 (CDW0):** Refer to Figure 95.|
|04|**Fabrics Command Type (FCTYPE):**This field specifies the Fabrics command transferred in the<br>capsule. The Fabrics command types are defined in Figure 541. If this field is set to a reserved value,<br>then the command shall be aborted with a status code of Invalid Field in Command. The format of the<br>FCTYPE field is shown here:<br>**Bits**<br>**Description**<br>07:02<br>**Function (FN):**This field contains a value that, in combination with the other fields in<br>the Fabrics Command Type data structure, creates a unique Combined Fabrics<br>Command Type.<br>01:00<br>**Data Transfer Direction (DTD):** This field indicates the direction of a data transfer, if<br>any.All options of the command shall transfer data as specified or transfer no<br>data. All commands, including vendor specific commands, shall follow this<br>convention. <br>**Value**<br>**Definition**<br>00b<br>**No Data Transfer:**No data is transferred.<br>01b<br>**Host to Controller Transfer:** Data is transferred from the host to the<br>controller.<br>10b<br>**Controller to Host Transfer:** Data is transferred from the controller to the<br>host.<br>11b<br>Reserved|
|23:05|Reserved|
|39:24|**SGL Descriptor 1 (SGL1):** This field contains a Transport SGL Data Block descriptor or a Keyed SGL<br>Data Block descriptor that describes the entire data transfer. Refer to section 4.3.2 for the definition of<br>SGL descriptors.<br>This field is used for Fabrics commands that transfer data. If a Fabrics command does not transfer data,<br>then this field is reserved.|
|63:40|**Fabrics Command Type Specific (FCTS):** This field is Fabrics command type specific.|


135


NVM Express [®] Base Specification, Revision 2.2


**Figure 95: Fabrics Command – Command Dword 0**







|Bits|Description|
|---|---|
|31:16|**Command Identifier (CID):** Refer to Figure 91.|
|15:14|**PRP or SGL for Data Transfer (PSDT):** <br>**Value**<br>**Definition**<br>00b<br>**No Data Transfered:**This value is used for Fabrics commands that do not transfer data.<br>If this value is used for Fabrics commands that transfer data, then SGLs are used for this<br>transfer. A host should use the value 10b rather than 00b for Fabrics commands that transfer<br>data.<br>01b<br>Reserved<br>10b<br>**Data Transferred:**This value is used for Fabrics commands that transfer data. SGLs are<br>used for this transfer.<br>11b<br>Reserved|
|13:10|Reserved|
|09:08|**Fused Operation (FUSE):** Refer to Figure 91. There are no fused Fabrics commands and as a result<br>this field is cleared to 00b.|
|07:00|**Opcode (OPC):** This field is set to 7Fh to specify a Fabrics command.|


|Value|Definition|
|---|---|
|00b|**No Data Transfered:**This value is used for Fabrics commands that do not transfer data.<br>If this value is used for Fabrics commands that transfer data, then SGLs are used for this<br>transfer. A host should use the value 10b rather than 00b for Fabrics commands that transfer<br>data.|
|01b|Reserved|
|10b|**Data Transferred:**This value is used for Fabrics commands that transfer data. SGLs are<br>used for this transfer.|
|11b|Reserved|


**4.2** **Completion Queue Entry**


**Admin Command and I/O Command Common CQE**


The Common Completion Queue Entry Layout is at least 16 bytes in size. Figure 96 describes the layout
of the first 16 bytes of the completion queue entry data structure which follows the Common Completion
Queue Entry Layout. The contents of Dword 0 and Dword 1 are command specific. If a command uses
Dword 0 or Dword 1, then the definition of these dwords is contained within the associated command
definition. If a command does not use Dword 0 or Dword 1, then the unused field(s) are reserved. Dword 2
is defined in Figure 97 and Dword 3 is defined in Figure 98.


If a completion queue entry is constructed via multiple writes, the Phase Tag bit shall be updated in the last
write of that completion queue entry.


**Figure 96: Common Completion Queue Entry Layout – Admin and All I/O Command Sets**

|Col1|31|23|Col4|15|7 0|
|---|---|---|---|---|---|
|**_DW0_**|Command Specific|Command Specific|Command Specific|Command Specific|Command Specific|
|**_DW1_**|Command Specific|Command Specific|Command Specific|Command Specific|Command Specific|
|**_DW2_**|SQ Identifier|SQ Identifier|SQ Identifier|SQ Head Pointer|SQ Head Pointer|
|**_DW3_**|Status|Status|P|Command Identifier|Command Identifier|



**Figure 97: Completion Queue Entry: DW 2**





|Bits|Description|
|---|---|
|31:16|**SQ Identifier (SQID):**Indicates the Submission Queue to which the associated command was issued.<br>This field is used by host software when more than one Submission Queue shares a single Completion<br>Queue to uniquely determine the command completed in combination with the Command Identifier (CID).<br>This is a reserved field in NVMe over Fabrics implementations.|
|15:00|**SQ Head Pointer (SQHD):**Indicates the current Submission Queue Head pointer for the Submission<br>Queue indicated in the SQ Identifier field. This is used to indicate to the host the submission queue entries<br>that have been consumed and may be re-used for new entries.<br>Note: The value returned is the value of the SQ Head pointer when the completion queue entry was<br>created. By the time host software consumes the completion queue entry, the controller may have an SQ<br>Head pointer that has advanced beyond the value indicated.|


136


NVM Express [®] Base Specification, Revision 2.2


**Figure 98: Completion Queue Entry: DW 3**





|Bits|Description|
|---|---|
|31:17|**Status (STATUS):**Indicates the status for the command that is being completed. Refer to section 4.2.3.|
|16|**Phase Tag (P):**Identifies whether a completion queue entry is new. Refer to section 4.2.4.<br>This is a reserved bit in NVMe over Fabrics implementations.|
|15:00|**Command Identifier (CID):**Indicates the identifier of the command that is being completed. This identifier<br>is assigned by host software when the command is submitted to the Submission Queue. The combination<br>of the SQ Identifier and Command Identifier uniquely identifies the command that is being completed. The<br>maximum number of requests outstanding for a Submission Queue at one time is 65,535.|


**Fabrics Command Common CQE**



The common completion queue entry for Fabrics commands is shown in Figure 99.


**Figure 99: Fabrics Response – Completion Queue Entry Format**






|Bytes|Description|
|---|---|
|07:00|**Fabrics Response Type Specific (FRTS):** The definition of this field is Fabrics response type<br>specific.|
|09:08|**SQ Head Pointer (SQHD):**This field indicates the current Submission Queue Head pointer for the<br>associated Submission Queue. This field is reserved if SQ flow control is disabled for the queue pair<br>(refer to section 6.3).|
|11:10|Reserved|
|13:12|**Command Identifier (CID):**This field indicates the identifier of the command that is being completed.|
|15:14|**Status Info (STS):** This field indicates the status for the associated Fabrics command.<br>**Bits**<br>**Description**<br>15:01<br>**Status (STATUS):** This field is defined in section 4.2.3.<br>00<br>Reserved|


|Bits|Description|
|---|---|
|15:01|**Status (STATUS):** This field is defined in section 4.2.3.|
|00|Reserved|



**Status Field Definition**


The Status field defines the status for the command indicated in the completion queue entry, defined in
Figure 100.


A value of 0h for the Status field indicates a successful command completion, with no fatal or non-fatal error
conditions. Unless otherwise noted, if a command fails to complete successfully for multiple reasons, then
the particular status code returned is chosen by the vendor.


**Figure 100: Completion Queue Entry: Status Field**





|Bits|Description|
|---|---|
|31|**Do Not Retry (DNR):**If this bit is set to ‘1’, then this bit indicates that if the same command is re-submitted<br>to any controller in the NVM subsystem, then that re-submitted command is expected to fail. If this bit is<br>cleared to ‘0’, then this bit indicates that the same command may succeed if retried. If a command is<br>aborted due to time limited error recovery (refer to the Error Recovery section in the NVM Command Set<br>Specification), this bit should be cleared to ‘0’. If the SCT and SC fields are cleared to 0h, then this bit<br>should be cleared to ‘0’.|
|30|**More (M):**If this bit is set to ‘1’, then there is more status information for this command as part of the Error<br>Information log page that may be retrieved with the Get Log Page command. If this bit is cleared to ‘0’,<br>then there is no additional status information for this command. Refer to section 5.1.12.1.2.|


137


NVM Express [®] Base Specification, Revision 2.2


**Figure 100: Completion Queue Entry: Status Field**







|Bits|Description|
|---|---|
|29:28|**Command Retry Delay (CRD):** If the DNR bit is cleared to ‘0’ and the host has set the Advanced<br>Command Retry Enable (ACRE) field to 1h in the Host Behavior Support feature (refer to section<br>5.1.25.1.14), then:<br>a)<br>a 00b CRD value indicates a command retry delay time of zero (i.e., the host may retry the<br>command immediately); and<br>b)<br>a non-zero CRD value selects a field in the Identify Controller data structure (refer to Figure 313)<br>that indicates the command retry delay time:<br>• <br>a 01b CRD value selects the Command Retry Delay Time 1 (CRDT1) field;<br>• <br>a 10b CRD value selects the Command Retry Delay Time 2 (CRDT2) field; and<br>• <br>a 11b CRD value selects the Command Retry Delay Time 3 (CRDT3) field.<br>The host should not retry the command until at least the amount of time indicated by the selected field has<br>elapsed. It is not an error for the host to retry the command prior to that time.<br>If the DNR bit is set to’1’ in the Status field or the ACRE field is cleared to 0h in the Host Behavior Support<br>feature, then this field is reserved.<br>If the SCT and SC fields are cleared to 0h, then this field should be cleared to 00b.|
|27:25|**Status Code Type (SCT):**Indicates the status code type of the completion queue entry. This indicates the<br>type of status code the controller is returning.|
|24:17|**Status Code (SC):**Indicates a status code identifying any error or status information for the command<br>indicated.|


Completion queue entries indicate a Status Code Type (SCT) for the type of completion being reported.
Figure 101 specifies the status code type values and descriptions.


**Figure 101: Status Code – Status Code Type Values**

















|Value|Definition|Reference|
|---|---|---|
|0h|**Generic Command Status:**Indicates that the command specified by the Command and<br>Submission Queue identifiers in the completion queue entry has completed. These status<br>values are generic across all command types, and include such conditions as success,<br>opcode not supported, and invalid field.|4.2.3.1|
|1h|**Command Specific Status:**Indicates a status value that is specific to a particular<br>command opcode. These values may indicate additional processing is required. Status<br>values such as invalid firmware image or exceeded maximum number of queues is<br>reported with this type.|4.2.3.2|
|2h|**Media and Data Integrity Errors:** Any media specific errors that occur in the NVM or data<br>integrity type errors shall be of this type.|4.2.3.3|
|3h|**Path Related Status:** Indicates that the command specified by the Command and<br>Submission Queue identifier in the completion queue entry has completed. These status<br>values are generic across all command types. These values may indicate that additional<br>process is required and indicate a status value that is specific to:<br>a)<br>the connection between the host and the controller processing the command; or<br>**b)**the characteristics that support Asymmetric Namespace Access Reporting (refer<br>to section 8.1.1), the characteristics of the relationship between the controller<br>processing the command and the specified namespace.|4.2.3.4|
|4h to 6h|Reserved|Reserved|
|7h|Vendor Specific|Vendor Specific|


The Status Code (SC) field in the completion queue entry indicates more detailed status information about
the completion being reported.


Each Status Code set of values is split into three ranges:

  - 00h to 7Fh: Applicable to Admin Command Set, or across multiple command sets;

  - 80h to BFh: I/O Command Set specific status codes; and


138


NVM Express [®] Base Specification, Revision 2.2


  - C0h to FFh: Vendor Specific status codes.


Unless otherwise specified, if multiple status codes apply, then the controller selects the status code that is
returned.


**Generic Command Status Definition**


Completion queue entries with a Status Code Type (SCT) of Generic Command Status indicate a status
value associated with the command that is generic across many different types of commands.


**Figure 102: Status Code – Generic Command Status Values**























|Value|Definition|I/O Command<br>1<br>Set(s)|
|---|---|---|
|00h|**Successful Completion:**The command completed without error.||
|01h|**Invalid Command Opcode:** A reserved coded value or an unsupported value in the<br>command opcode field.||
|02h|**Invalid Field in Command:** A reserved coded value or an unsupported value in a<br>defined field (other than the opcode field). This status code should be used unless<br>another status code is explicitly specified for a particular condition. The field may be in<br>the command parameters as part of the submission queue entry or in data structures<br>pointed to by the command parameters.||
|03h|**Command ID Conflict:** The command identifier is already in use. Note: It is<br>implementation specific how many commands are searched for a conflict.||
|04h|**Data Transfer Error:** Transferring the data or metadata associated with a command<br>had an error.||
|05h|**Commands Aborted due to Power Loss Notification:** Indicates that the command<br>was aborted due to a power loss notification.||
|06h|**Internal Error:** The command was not completed successfully due to an internal error.<br>Details on the internal device error should be reported as an asynchronous event.<br>Refer to Figure 150 for Internal Error Asynchronous Event Information.||
|07h|**Command Abort Requested:** The command was aborted due to:<br>• <br>an Abort command being received that specified this command (refer to<br>section 5.1.1); or<br>• <br>a Cancel command being received that specified this command (refer to<br>section 7.1).||
|08h|**Command Aborted due to SQ Deletion:** The command was aborted due to a Delete<br>I/O Submission Queue request received for the Submission Queue to which the<br>command was submitted.||
|09h|**Command Aborted due to Failed Fused Command:** The command was aborted<br>due to the other command in a fused operation failing.||
|0Ah|**Command Aborted due to Missing Fused Command:** The fused command was<br>aborted due to the adjacent submission queue entry not containing a fused command<br>that is the other command in a supported fused operation (refer to section 3.4.2).||
|0Bh|**Invalid Namespace or Format:**The namespace or the format of that namespace is<br>invalid.||
|0Ch|**Command Sequence Error:**The command was aborted due to a protocol violation in<br>a multi-command sequence (e.g., a violation of the Security Send and Security Receive<br>sequencing rules in the TCG Storage Synchronous Interface Communications protocol<br>(refer to TCG Storage Architecture Core Specification)).||
|0Dh|**Invalid SGL Segment Descriptor:** The command includes an invalid SGL Last<br>Segment or SGL Segment descriptor. This may occur under various conditions,<br>including:<br>a)<br>the SGL segment pointed to by an SGL Last Segment descriptor contains an<br>SGL Segment descriptor or an SGL Last Segment descriptor; <br>b)<br>an SGL Last Segment descriptor contains an invalid length (i.e., a length of<br>0h or 1h that is not a multiple of 16); or <br>c)<br>an SGL Segment descriptor or an SGL Last Segment descriptor contains an<br>invalid address (e.g., an address that is not qword aligned).||


139


NVM Express [®] Base Specification, Revision 2.2


**Figure 102: Status Code – Generic Command Status Values**





























|Value|Definition|I/O Command<br>1<br>Set(s)|
|---|---|---|
|0Eh|**Invalid Number of SGL Descriptors:** There is an SGL Last Segment descriptor or an<br>SGL Segment descriptor in a location other than the last descriptor of a segment based<br>on the length indicated. This is also used for invalid SGLs in a command capsule.||
|0Fh|**Data SGL Length Invalid:** This may occur if the length of a data SGL is too short. This<br>may occur if the length of a data SGL is too long and the controller does not support<br>SGL lengths longer than the requested data transfer length (refer to section 4.3.2) as<br>indicated in the SGL Support field of the Identify Controller data structure.||
|10h|**Metadata SGL Length Invalid:** This may occur if the length of a metadata SGL is too<br>short. This may occur if the length of a metadata SGL is too long and the controller<br>does not support SGL lengths longer than the requested data transfer length (refer to<br>section 4.3.2) as indicated in the SGL Support field of the Identify Controller data<br>structure.||
|11h|**SGL Descriptor Type Invalid:** The type of an SGL Descriptor is a type that is not<br>supported by the controller, or the combination of type and subtype is not supported<br>by the controller.||
|12h|**Invalid Use of Controller Memory Buffer:**The attempted use of the Controller<br>Memory Buffer is not supported by the controller. Refer to section 8.2.1.||
|13h|**PRP Offset Invalid:**The Offset field for a PRP entry is invalid. This may occur when<br>there is a PRP entry with a non-zero offset after the first entry or when the Offset field<br>in any PRP entry is not dword aligned (i.e., bits 1:0 are not cleared to 00b).||
|14h|**Atomic Write Unit Exceeded:**See the applicable I/O Command Set specification for<br>the description.|NVM, ZNS|
|15h|**Operation Denied:**The command was denied due to lack of access rights. Refer to<br>the appropriate security specification (e.g., TCG Storage Interface Interactions<br>specification). For media access commands, the Access Denied status code should<br>be used instead.||
|16h|**SGL Offset Invalid:**The offset specified in an SGL descriptor is invalid. This may<br>occur when using capsules for data transfers in NVMe over Fabrics implementations<br>and an invalid offset in the capsule is specified.||
|17h|Reserved||
|18h|**Host Identifier Inconsistent Format:**The NVM subsystem detected the simultaneous<br>use of 64-bit and 128-bit Host Identifier values on different controllers.||
|19h|**Keep Alive Timer Expired:**The Keep Alive Timer expired.||
|1Ah|**Keep Alive Timeout Invalid:**The Keep Alive Timeout value specified is invalid. This<br>may be due to an attempt to specify a value of 0h on a transport that requires the Keep<br>Alive Timer feature to be enabled. This may be due to the value specified being too<br>large for the associated NVMe Transport as defined in the NVMe Transport binding<br>specification.||
|1Bh|**Command Aborted due to Preempt and Abort:** The command was aborted due to<br>a Reservation Acquire command with the Reservation Acquire Action (RACQA) set to<br>010b (Preempt and Abort).||
|1Ch|**Sanitize Failed:**The most recent sanitize operation failed and no recovery action has<br>been successfully completed.||
|1Dh|**Sanitize In Progress:**The requested function (e.g., command) is prohibited while a<br>sanitize operation is in progress. Refer to section 8.1.24.4.||
|1Eh|**SGL Data Block Granularity Invalid:**See the applicable I/O Command Set<br>specification for the description.|NVM, ZNS|
|1Fh|**Command Not Supported for Queue in CMB:** The implementation does not support<br>submission of the command to a Submission Queue in the Controller Memory Buffer<br>or command completion to a Completion Queue in the Controller Memory Buffer.<br>Note: NVM Express revision 1.3 and later use this status code only for Sanitize<br>commands.||
|20h|**Namespace is Write Protected:** The command is prohibited while the namespace is<br>write protected as a result of a change in the namespace write protection state as<br>defined by the Namespace Write Protection State Machine (refer to Figure 623).||


140


NVM Express [®] Base Specification, Revision 2.2


**Figure 102: Status Code – Generic Command Status Values**




















|Value|Definition|I/O Command<br>1<br>Set(s)|
|---|---|---|
|21h|**Command Interrupted:** Command processing was interrupted and the controller is<br>unable to successfully complete the command. The host should retry the command.<br>If this status code is returned, then the controller shall clear the Do Not Retry bit to ‘0’<br>in the Status field of the CQE (refer to Figure 100). The controller shall not return this<br>status code unless the host has set the Advanced Command Retry Enable (ACRE)<br>field to 1h in the Host Behavior Support feature (refer to section 5.1.25.1.14).||
|22h|**Transient Transport Error:** A transient transport error was detected. If the command<br>is retried on the same controller, the command is likely to succeed. A command that<br>fails with a transient transport error four or more times should be treated as a persistent<br>transport error that is not likely to succeed if retried on the same controller.||
|23h|**Command Prohibited by Command and Feature Lockdown:**The command was<br>aborted due to command execution being prohibited by the Command and Feature<br>Lockdown (refer to section 8.1.5).||
|24h|**Admin Command Media Not Ready:**The Admin command requires access to media<br>and the media is not ready. The Do Not Retry bit indicates whether re-issuing the<br>command at a later time may succeed. This status code shall only be returned:<br>a)<br>for Admin commands; and<br>b)<br>if the controller is in Controller Ready Independent of Media mode (i.e.,<br>CC.CRIME bit is set to ‘1’).<br>This status code shall not be returned with the Do Not Retry bit cleared to ‘0’ after the<br>amount of time indicated by the Controller Ready With Media Timeout<br>(CRTO.CRWMT) field after the controller is enabled (i.e., CC.EN transitions from ‘0’ to<br>‘1’).<br>Refer to Figure 84 for the list of Admin commands permitted to return this status code.||
|25h|**Invalid Key Tag:**The command was aborted due to an invalid KEYTAG field value<br>(refer to Figure 621) as:<br>a)<br>the value of the specified KEYTAG field is greater than the Maximum Key Tag<br>(MAXKT) field in the I/O Command Set Independent Identify Namespace data<br>structure (refer to Figure 320); or<br>b)<br>defined by the appropriate security specification (e.g., TCG Storage Interface<br>Interactions specification).||
|26h|**Host Dispersed Namespace Support Not Enabled:** The command is prohibited<br>while the Host Dispersed Namespace Support (HDISNS) field is not set to 1h in the<br>Host Behavior Support feature (refer to Figure 408).||
|27h|**Host Identifier Not Initialized**||
|28h|**Incorrect Key:**The command was aborted due to the key associated with the<br>KEYTAG field being incorrect.<br>The specific conditions under which a key is considered incorrect are defined by the<br>appropriate security specification (e.g., TCG Storage Interface Interactions<br>specification).||
|29h|**FDP Disabled:**The command is not allowed when Flexible Data Placement is<br>disabled.||
|2Ah|**Invalid Placement Handle List**: The Placement Handle List is invalid due to:<br>• <br>a Reclaim Unit Handle Identifier that is:<br>`o` valid but restricted to be used by the command; or<br>`o` invalid;<br>or<br>• the Placement Handle List number of entries exceeded the maximum<br>number allowed.||
|2Bh to 7Fh|Reserved||



141


NVM Express [®] Base Specification, Revision 2.2


**Figure 102: Status Code – Generic Command Status Values**















|Value|Definition|I/O Command<br>1<br>Set(s)|
|---|---|---|
|80h|**LBA Out of Range:** See the applicable I/O Command Set specification for the<br>description.|NVM, ZNS|
|81h|**Capacity Exceeded:** The command attempted an operation that exceeds the capacity<br>of the namespace.||
|82h|**Namespace Not Ready:** The namespace is not ready to be accessed as a result of a<br>condition other than a condition that is reported as an Asymmetric Namespace Access<br>condition. The Do Not Retry bit indicates whether re-issuing the command at a later<br>time may succeed.||
|83h|**Reservation Conflict:** The command was aborted due to a conflict with a reservation<br>held on the accessed namespace. Refer to section 8.1.22.||
|84h|**Format In Progress:** A Format NVM command is in progress on the namespace. The<br>Do Not Retry bit shall be cleared to ‘0’ to indicate that the command may succeed if<br>resubmitted.|NVM, ZNS|
|85h|**Invalid Value Size:** See the applicable I/O Command Set specification for the<br>description.|KV|
|86h|**Invalid Key Size:** See the applicable I/O Command Set specification for the<br>description.|KV|
|87h|**KV Key Does Not Exist:** See the applicable I/O Command Set specification for the<br>description.|KV|
|88h|**Unrecovered Error:** See the applicable I/O Command Set specification for the<br>description.|KV|
|89h|**Key Exists:**See the applicable I/O Command Set specification for the description.|KV|
|90h to BFh|Reserved||
|C0h to FFh|Vendor Specific||
|Key:<br>NVM – NVM Command Set<br>ZNS – Zoned Namespace Command Set<br>KV – Key Value Command Set<br>Notes:<br>1.<br>This column is blank unless the value is I/O Command Set specific|Key:<br>NVM – NVM Command Set<br>ZNS – Zoned Namespace Command Set<br>KV – Key Value Command Set<br>Notes:<br>1.<br>This column is blank unless the value is I/O Command Set specific|Key:<br>NVM – NVM Command Set<br>ZNS – Zoned Namespace Command Set<br>KV – Key Value Command Set<br>Notes:<br>1.<br>This column is blank unless the value is I/O Command Set specific|


**Command Specific Status Definition**


Completion queue entries with a Status Code Type (SCT) of Command Specific Errors indicate an error
that is specific to a particular command opcode. Status codes of 00h to 7Fh are for Admin command errors.
Status codes of 80h to BFh are specific to the selected I/O command sets.


**Figure 103: Status Code – Command Specific Status Values**







|Value|Description|Commands Affected|
|---|---|---|
|00h|Completion Queue Invalid|Create I/O Submission Queue|
|01h|Invalid Queue Identifier|Create I/O Submission Queue,<br>Create I/O Completion Queue,<br>Delete I/O Completion Queue,<br>Delete I/O Submission Queue|
|02h|Invalid Queue Size|Create I/O Submission Queue,<br>Create I/O Completion Queue|
|03h|Abort Command Limit Exceeded|Abort|
|04h|Reserved||
|05h|Asynchronous Event Request Limit Exceeded|Asynchronous Event Request|
|06h|Invalid Firmware Slot|Firmware Commit|
|07h|Invalid Firmware Image|Firmware Commit|
|08h|Invalid Interrupt Vector|Create I/O Completion Queue|
|09h|Invalid Log Page|Get Log Page|


142


NVM Express [®] Base Specification, Revision 2.2


**Figure 103: Status Code – Command Specific Status Values**


















|Value|Description|Commands Affected|
|---|---|---|
|0Ah|Invalid Format|Format<br>NVM,<br>Namespace<br>Management|
|0Bh|Firmware Activation Requires Conventional Reset|Firmware Commit, Sanitize|
|0Ch|Invalid Queue Deletion|Delete I/O Completion Queue|
|0Dh|Feature Identifier Not Saveable|Set Features|
|0Eh|Feature Not Changeable|Set Features|
|0Fh|Feature Not Namespace Specific|Set Features|
|10h|Firmware Activation Requires NVM Subsystem<br>Reset|Firmware Commit, Sanitize|
|11h|Firmware Activation Requires Controller Level<br>Reset|Firmware Commit, Sanitize|
|12h|Firmware Activation Requires Maximum Time<br>Violation|Firmware Commit|
|13h|Firmware Activation Prohibited|Firmware Commit|
|14h|Overlapping Range|Firmware Commit, Firmware<br>Image Download, Set Features|
|15h|Namespace Insufficient Capacity|Namespace Management|
|16h|Namespace Identifier Unavailable|Namespace Management|
|17h|Reserved||
|18h|Namespace Already Attached|Namespace Attachment|
|19h|Namespace Is Private|Namespace Attachment|
|1Ah|Namespace Not Attached|Namespace Attachment|
|1Bh|Thin Provisioning Not Supported|Namespace Management|
|1Ch|Controller List Invalid|Namespace Attachment|
|1Dh|Device Self-test In Progress|Device Self-test|
|1Eh|Boot Partition Write Prohibited|Firmware Commit|
|1Fh|Invalid Controller Identifier|Virtualization Management, Track<br>Send, Track Receive, Migration<br>Send, Migration<br>Receive,Controller Data Queue|
|20h|Invalid Secondary Controller State|Virtualization Management|
|21h|Invalid Number of Controller Resources|Virtualization Management|
|22h|Invalid Resource Identifier|Virtualization Management|
|23h|Sanitize Prohibited While Persistent Memory<br>Region is Enabled|Sanitize|
|24h|ANA Group Identifier Invalid|Namespace Management|
|25h|ANA Attach Failed|Namespace Attachment|
|26h|Insufficient Capacity|Capacity Management|
|27h|Namespace Attachment Limit Exceeded|Namespace Attachment|
|28h|Prohibition of Command Execution Not Supported|Lockdown|
|29h|I/O Command Set Not Supported|Namespace Attachment,<br>Namespace Management|
|2Ah|I/O Command Set Not Enabled|Namespace Attachment|
|2Bh|I/O Command Set Combination Rejected|Set Features|
|2Ch|Invalid I/O Command Set|Identify|
|2Dh|Identifier Unavailable|Capacity Management|
|2Eh|Namespace Is Dispersed|Reservation Acquire, Reservation<br>Register, Reservation Release,<br>Reservation Report|
|2Fh|Invalid Discovery Information|Discovery Information<br>Management|
|30h|Zoning Data Structure Locked|Fabric Zoning Lookup, Fabric<br>Zoning Send, Fabric Zoning<br>Receive|



143


NVM Express [®] Base Specification, Revision 2.2


**Figure 103: Status Code – Command Specific Status Values**







|Value|Description|Commands Affected|
|---|---|---|
|31h|Zoning Data Structure Not Found|Fabric Zoning Lookup, Fabric<br>Zoning Send, Fabric Zoning<br>Receive|
|32h|Insufficient Discovery Resources|Discovery Information<br>Management|
|33h|Requested Function Disabled|Fabric Zoning Lookup, Fabric<br>Zoning Send, Fabric Zoning<br>Receive|
|34h|ZoneGroup Originator Invalid|Fabric Zoning Send|
|35h|Invalid Host|Manage Exported NVM<br>Subsystem|
|36h|Invalid NVM Subsystem|Manage Exported NVM<br>Subsystem|
|37h|Invalid Controller Data Queue|Set Features, Get Features, Track<br>Send, Controller Data Queue|
|38h|Not Enough Resources|Track Send, Controller Data<br>Queue|
|39h|Controller Suspended|Track Send, Sanitize|
|3Ah|Controller Not Suspended|Track Send|
|3Bh|Controller Data Queue Full|Track Send|
|3Ch to 6Fh|Reserved||
|70h to 7Fh|Directive Specific|NOTE 1|
|80h to BFh|I/O Command Set Specific|Refer to Figure 104|
|C0h to FFh|Vendor Specific||
|Notes:<br>1.<br>The Directives Specific range defines Directives specific status values. Refer to section 8.1.8.|Notes:<br>1.<br>The Directives Specific range defines Directives specific status values. Refer to section 8.1.8.|Notes:<br>1.<br>The Directives Specific range defines Directives specific status values. Refer to section 8.1.8.|


**Figure 104: Status Code – Command Specific Status Values, I/O Commands**

|Value|Definition|
|---|---|
|80h|Conflicting Attributes|
|81h|Invalid Protection Information|
|82h|Attempted Write to Read Only Range|
|83h|Command Size Limit Exceeded|
|84h|Invalid Command ID|
|85h|Incompatible Namespace or Format|
|86h|Fast Copy Not Possible|
|87h|Overlapping I/O Range|
|88h|Namespace Not Reachable|
|89h|Insufficient Resources|
|8Ah|Insufficient Program Resources|
|8Bh|Invalid Memory Namespace|
|8Ch|Invalid Memory Range Set|
|8Dh|Invalid Memory Range Set Identifier|
|8Eh|Invalid Program Data|
|8Fh|Invalid Program Index|
|90h|Invalid Program Type|
|91h|Maximum Memory Ranges Exceeded|
|92h|Maximum Memory Range Sets Exceeded|
|93h|Maximum Programs Activated|
|94h|Maximum Program Bytes Exceeded|
|95h|Memory Range Set In Use|
|96h|No Program|
|97h|Overlapping Memory Ranges|
|98h|Program Not Activated|



144


NVM Express [®] Base Specification, Revision 2.2


**Figure 104: Status Code – Command Specific Status Values, I/O Commands**

|Value|Definition|
|---|---|
|99h|Program In Use|
|9Ah|Program Index Not Downloadable|
|9Bh|Program Too Big|
|9Ch|Successful Media Verification Read|
|9Dh to B7h|Reserved|
|B8h|Zoned Boundary Error|
|B9h|Zone Is Full|
|BAh|Zone Is Read Only|
|BBh|Zone Is Offline|
|BCh|Zone Invalid Write|
|BDh|Too Many Active Zones|
|BEh|Too Many Open Zones|
|BFh|Invalid Zone State Transition|



**Figure 105: Status Code – Command Specific Status Values, Fabrics Commands**



























|Value|Definition|Commands<br>Affected|
|---|---|---|
|80h|**Incompatible Format:** The NVM subsystem does not support the record format<br>specified by the host.|Connect,<br>Disconnect|
|81h|**Controller Busy:**The controller is already associated with a host (Connect<br>command). This value is also returned if there is no available controller (Connect<br>command).<br>The controller is not able to disconnect the I/O Queue at the current time (Disconnect<br>command).|Connect,<br>Disconnect|
|82h|**Connect Invalid Parameters:**One or more of the command parameters (e.g., Host<br>NQN, NVM Subsystem NQN, Host Identifier, Controller ID, Queue ID) specified are<br>not valid.|Connect|
|83h|**Connect Restart Discovery:**The NVM subsystem requested is not available. The<br>host should restart the discovery process.|Connect|
|84h|**Connect Invalid Host:**The host is not allowed to establish an association to any<br>controller in the NVM subsystem or the host is not allowed to establish an<br>association to the specified controller.|Connect|
|85h|**Invalid Queue Type:**The command was sent on the wrong queue type (e.g., a<br>Disconnect command was sent on the Admin queue).|Disconnect|
|86h to 8Fh|Reserved|Reserved|
|90h|**Discover Restart:**The snapshot of the records is now invalid or out of date. If the<br>Discovery log page was requested, then the host or Discovery controller should re-<br>read the Discovery log page. If the Host Discovery log page was requested, then<br>the host or Discovery controller should re-read the Host Discovery log page.|Get Log Page|
|91h|**Authentication Required:**NVMe in-band authentication is required and the queue<br>has not yet been authenticated.|NOTE 1|
|92h to AFh|Reserved|Reserved|
|B0h to BFh|**Transport Specific:** The status values in this range are NVMe Transport specific. Refer to the<br>appropriate NVMe Transport binding specification for the definition of these status values.|**Transport Specific:** The status values in this range are NVMe Transport specific. Refer to the<br>appropriate NVMe Transport binding specification for the definition of these status values.|
|Notes:<br>1.<br>All commands other than Connect, Authenticate Send, and Authenticate Receive.|Notes:<br>1.<br>All commands other than Connect, Authenticate Send, and Authenticate Receive.|Notes:<br>1.<br>All commands other than Connect, Authenticate Send, and Authenticate Receive.|


**Media and Data Integrity Errors Definition**


Completion queue entries with a Status Code Type (SCT) of Media and Data Integrity Errors indicate an
error associated with the command that is due to an error associated with the NVM media or a data integrity
type error.


145


NVM Express [®] Base Specification, Revision 2.2


**Figure 106: Status Code – Media and Data Integrity Error Values**







|Value|Definition|1<br>Command Set(s)|
|---|---|---|
|00h to 7Fh|Reserved||
|80h|**Write Fault:**The write data could not be committed to the media.||
|81h|**Unrecovered Read Error:**The read data could not be recovered from the<br>media.||
|82h|**End-to-end Guard Check Error:**The command was aborted due to an end-<br>to-end guard check failure.||
|83h|**End-to-end Application Tag Check Error:**The command was aborted due to<br>an end-to-end application tag check failure.||
|84h|**End-to-end Reference Tag Check Error:**The command was aborted due to<br>an end-to-end reference tag check failure.||
|85h|**Compare Failure:**See the NVM Command Set Specification for the<br>description.|NVM|
|86h|**Access Denied:**Access to the namespace and/or user data is denied due to<br>lack of access rights. Refer to the appropriate security specification (e.g., TCG<br>Storage Interface Interactions Specification).||
|87h|**Deallocated or Unwritten Logical Block:**See the NVM Command Set<br>Specification for the description.|NVM|
|88h|**End-to-End Storage Tag Check Error:**The command was aborted due to an<br>end-to-end storage tag check failure.||
|89h to BFh|Reserved||
|C0h to FFh|Vendor Specific||
|Key:<br>NVM – NVM Command Set<br>Notes:<br>1.<br>This column is blank unless the value is I/O Command Set specific.|Key:<br>NVM – NVM Command Set<br>Notes:<br>1.<br>This column is blank unless the value is I/O Command Set specific.|Key:<br>NVM – NVM Command Set<br>Notes:<br>1.<br>This column is blank unless the value is I/O Command Set specific.|


**Path Related Status Definition**


Completion queue entries with a Status Code Type (SCT) of Path Related Status (refer to Figure 107)
indicate a status value associated with the command that is generic across many different types of
commands and applies to a specific connection between the host and controller processing the command
or between the controller and the namespace. The command for which this status is returned may be retried
on a different controller in the same NVM subsystem if more than one controller is available to the host.


In a multipath environment, unless otherwise specified, errors of this type should be retried using a different
path, if one is available.


**Figure 107: Status Code – Path Related Status Values**







|Value|Definition|
|---|---|
|00h|**Internal Path Error:** The command was not completed as the result of a controller internal error<br>that is specific to the controller processing the command. Retries for the request function should be<br>based on the setting of the DNR bit (refer to Figure 100).|
|01h|**Asymmetric Access Persistent Loss:** The requested function (e.g., command) is not able to be<br>performed as a result of the relationship between the controller and the namespace, NVM Set, or<br>Endurance Group being in the ANA Persistent Loss state (refer to section 8.1.1.7). The command<br>should not be re-submitted to the same controller.|
|02h|**Asymmetric Access Inaccessible:** The requested function (e.g., command) is not able to be<br>performed as a result of the relationship between the controller and the namespace, NVM Set, or<br>Endurance Group being in the ANA Inaccessible state (refer to section 8.1.1.6). The command<br>should not be re-submitted to the same controller.|
|03h|**Asymmetric Access Transition:** The requested function (e.g., command) is not able to be<br>performed as a result of the relationship between the controller and the namespace, NVM Set, or<br>Endurance Group transitioning between Asymmetric Namespace Access states (refer to section<br>8.1.1.8). The requested function should be retried after the transition is complete.|
|04h to 5Fh|Reserved|


146


NVM Express [®] Base Specification, Revision 2.2


**Figure 107: Status Code – Path Related Status Values**

|Value|Definition|
|---|---|
|**Controller detected Pathing errors**|**Controller detected Pathing errors**|
|60h|**Controller Pathing Error:** A pathing error was detected by the controller.|
|61h to 6Fh|Reserved|
|**Host detected Pathing errors**|**Host detected Pathing errors**|
|70h|**Host Pathing Error:** A pathing error was detected by the host.|
|71h|**Command Aborted By Host:** The command was aborted as a result of host action (e.g., the host<br>disconnected the fabric connection).|
|72h to 7Fh|Reserved|
|**Other Pathing errors**|**Other Pathing errors**|
|80h to BFh|I/O Command Set Specific|
|C0h to FFh|Vendor Specific|



**Phase Tag**


The Phase Tag bit indicates whether a completion queue entry is new. The Phase Tag bit for each
completion queue entry in:

  - the Admin Completion Queue shall be initialized to ‘0’ by the host prior to setting CC.EN (refer to
Figure 41) to ‘1’; and

  - an I/O Completion Queue shall be initialized to ‘0’ by the host prior to submitting the Create I/O
Completion Queue command for that queue.


When the controller posts a new completion queue entry to the Completion Queue, the controller shall
invert the Phase Tag bit in that completion queue entry (i.e., the inverting of the Phase Tag bit enables the
host to detect the new completion queue entry).


When a completion queue entry is posted to a completion queue slot in:

  - the Admin Completion Queue for the first time after CC.EN is set to ‘1’, the Phase Tag bit for that
completion queue entry is set to ‘1’; and

  - an I/O Completion Queue for the first time after the Create I/O Completion Queue command
completed for that queue, the Phase Tag bit for that completion queue entry is set to ‘1’.


This continues for each completion queue entry that is posted until the controller posts a completion queue
entry to the highest numbered completion queue slot and wraps to completion queue slot number 0 as
described in section 3.3.1.2. When that queue wrap condition occurs, the Phase Tag bit is then cleared to
‘0’ in each completion queue entry that is posted. This continues until another queue wrap condition occurs.
Each time a queue wrap condition occurs, the value of the Phase Tag bit is inverted (i.e., changes from ‘1’
to ‘0’ or changes from ‘0’ to ‘1’).


**Phase Tag Example**


Figure 108 shows an example of how the Phase Tag bit changes over time as a memory-based controller
completes commands and the host processes those completions. This example shows a Completion
Queue consisting of 6 entries.


147


NVM Express [®] Base Specification, Revision 2.2


**Figure 108: Phase Tag bit Transition Example**

















































|1<br>T|Condition|Completion Queue Entry/Slot number|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|**T1**|**Condition**|**0**|**1**|**2**|**3**|**4**|**5**|
|0|Admin Queue: Host initializes<br>Completion Queue and sets CC.EN<br>to ‘1’<br>I/O Queue: Host initializes<br>Completion Queue and submits<br>Create I/O Completion Queue<br>command|P(0) (E)<br>HEAD-><br>TAIL->|P(0)<br>(E)|P(0)<br>(E)|P(0)<br>(E)|P(0)<br>(E)|P(0)<br>(E)|
|1|Controller has completed 1<br>command and the host has<br>consumed 0 completions|P(1)<br>HEAD->|P(0) (E)<br>TAIL->|P(0)<br>(E)|P(0)<br>(E)|P(0)<br>(E)|P(0)<br>(E)|
|2|Controller has completed 6<br>commands and the host has<br>consumed 2 completions|P(1) (E)<br>TAIL->|P(1)<br>(E)|P(1)<br>HEAD->|P(1)|P(1)|P(1)|
|3|Controller has completed 7<br>commands and the host has<br>consumed 2 completions|P(0)|P(1) (E)<br>TAIL->|P(1)<br>HEAD->|P(1)|P(1)|P(1)|
|4|Controller has completed 7<br>commands and the host has<br>consumed 4 completions|P(0)|P(1) (E)<br>TAIL->|P(1)<br>(E)|P(1)<br>(E)|P(1)<br>HEAD->|P(1)|
|5|Controller has completed 11<br>commands and the host has<br>consumed 8 completions|P(0)<br>(E)|P(0)<br>(E)|P(0)<br>HEAD->|P(0)|P(0)|P(1) (E)<br>TAIL->|
|6|Controller has completed 11<br>commands and the host has<br>consumed 11 completions|P(0)<br>(E)|P(0)<br>(E)|P(0)<br>(E)|P(0)<br>(E)|P(0)<br>(E)|P(1) (E)<br>HEAD-><br>TAIL->|
|Key:<br>P(0) =<br>Phase Tag bit for this completion queue entry is cleared to the value ‘0’.<br>P(1) =<br>Phase Tag bit for this completion queue entry is set to the value ‘1’.<br>(E) =<br>The Entry/Slot is empty.<br>HEAD-> =<br>Completion Queue Head Pointer for this completion queue is set to indicate this slot.<br>TAIL-> =<br>Completion Queue Tail Pointer for this completion queue is used within the controller to indicate this<br>slot.<br>Note:<br>1.<br>T = Time sequence.|Key:<br>P(0) =<br>Phase Tag bit for this completion queue entry is cleared to the value ‘0’.<br>P(1) =<br>Phase Tag bit for this completion queue entry is set to the value ‘1’.<br>(E) =<br>The Entry/Slot is empty.<br>HEAD-> =<br>Completion Queue Head Pointer for this completion queue is set to indicate this slot.<br>TAIL-> =<br>Completion Queue Tail Pointer for this completion queue is used within the controller to indicate this<br>slot.<br>Note:<br>1.<br>T = Time sequence.|Key:<br>P(0) =<br>Phase Tag bit for this completion queue entry is cleared to the value ‘0’.<br>P(1) =<br>Phase Tag bit for this completion queue entry is set to the value ‘1’.<br>(E) =<br>The Entry/Slot is empty.<br>HEAD-> =<br>Completion Queue Head Pointer for this completion queue is set to indicate this slot.<br>TAIL-> =<br>Completion Queue Tail Pointer for this completion queue is used within the controller to indicate this<br>slot.<br>Note:<br>1.<br>T = Time sequence.|Key:<br>P(0) =<br>Phase Tag bit for this completion queue entry is cleared to the value ‘0’.<br>P(1) =<br>Phase Tag bit for this completion queue entry is set to the value ‘1’.<br>(E) =<br>The Entry/Slot is empty.<br>HEAD-> =<br>Completion Queue Head Pointer for this completion queue is set to indicate this slot.<br>TAIL-> =<br>Completion Queue Tail Pointer for this completion queue is used within the controller to indicate this<br>slot.<br>Note:<br>1.<br>T = Time sequence.|Key:<br>P(0) =<br>Phase Tag bit for this completion queue entry is cleared to the value ‘0’.<br>P(1) =<br>Phase Tag bit for this completion queue entry is set to the value ‘1’.<br>(E) =<br>The Entry/Slot is empty.<br>HEAD-> =<br>Completion Queue Head Pointer for this completion queue is set to indicate this slot.<br>TAIL-> =<br>Completion Queue Tail Pointer for this completion queue is used within the controller to indicate this<br>slot.<br>Note:<br>1.<br>T = Time sequence.|Key:<br>P(0) =<br>Phase Tag bit for this completion queue entry is cleared to the value ‘0’.<br>P(1) =<br>Phase Tag bit for this completion queue entry is set to the value ‘1’.<br>(E) =<br>The Entry/Slot is empty.<br>HEAD-> =<br>Completion Queue Head Pointer for this completion queue is set to indicate this slot.<br>TAIL-> =<br>Completion Queue Tail Pointer for this completion queue is used within the controller to indicate this<br>slot.<br>Note:<br>1.<br>T = Time sequence.|Key:<br>P(0) =<br>Phase Tag bit for this completion queue entry is cleared to the value ‘0’.<br>P(1) =<br>Phase Tag bit for this completion queue entry is set to the value ‘1’.<br>(E) =<br>The Entry/Slot is empty.<br>HEAD-> =<br>Completion Queue Head Pointer for this completion queue is set to indicate this slot.<br>TAIL-> =<br>Completion Queue Tail Pointer for this completion queue is used within the controller to indicate this<br>slot.<br>Note:<br>1.<br>T = Time sequence.|Key:<br>P(0) =<br>Phase Tag bit for this completion queue entry is cleared to the value ‘0’.<br>P(1) =<br>Phase Tag bit for this completion queue entry is set to the value ‘1’.<br>(E) =<br>The Entry/Slot is empty.<br>HEAD-> =<br>Completion Queue Head Pointer for this completion queue is set to indicate this slot.<br>TAIL-> =<br>Completion Queue Tail Pointer for this completion queue is used within the controller to indicate this<br>slot.<br>Note:<br>1.<br>T = Time sequence.|


At time 0, the host initializes the Completion queue (i.e., clearing the Phase Tag bit to ‘0’ in each completion
queue entry in the completion queue). For the Admin Completion Queue, the host then sets CC.EN to ‘1’
to enable the controller. For an I/O Completion Queue, the host then sends the Create I/O Completion
Queue command. The queue, at this time, is in the Empty condition (refer to section 3.3.1.4).


At time 1, the controller has completed a command, but the host has not consumed that completion queue
entry. As a result of the command completion, the Phase Tag bit in completion queue entry 0 has been
inverted to ‘1’. Since no completion queue entries have been consumed, the Completion Queue Head
pointer still indicates completion queue entry 0. The controller has updated the internal Completion Queue
Tail Pointer to indicate that completion queue slot 1 is the next completion queue slot into which the
controller posts a completion queue entry.


At time 2, the controller has completed 5 additional commands (i.e., 6 commands have been completed)
and the host has consumed 2 of the completion queue entries. As a result of the 5 additional commands
having been completed, the Phase Tag bit has been inverted to ‘1’ in completion queue entry 1 through
completion queue entry 5. As a result of 2 completion queue entries having been consumed, the host has
updated the Completion Queue Head Pointer to indicate that completion queue entry 0 and completion
queue entry 1 have been consumed (i.e., completion queue entry 2 is the next completion queue entry for
the host to consume). The controller has updated the internal Completion Queue Tail Pointer to indicate


148


NVM Express [®] Base Specification, Revision 2.2


that completion queue slot 0 is the next completion queue slot into which the controller posts a completion
queue entry.


At time 3, the controller has completed 1 additional command (i.e., 7 commands have been completed) and
no additional completion queue entries have been consumed by the host (i.e., 2 completion queue entries
have been consumed). As a result of the additional command having been completed, the Phase Tag bit
has been inverted to ‘0’ in completion queue entry 0 (i.e., accounting for the queue wrap condition). The
controller has updated the internal Completion Queue Tail Pointer to indicate that completion queue slot 1
is the next completion queue slot into which the controller posts a completion queue entry **.** The queue, at
this time, is in the Full condition (refer to section 3.3.1.5).


At time 4, the controller has completed no additional commands (i.e., 7 commands have been completed)
and the host has consumed 2 additional completion queue entries (i.e., 4 completion queue entries have
been consumed). As a result of 2 additional completion queue entries having been consumed, the host has
updated the Completion Queue Head Pointer to indicate that completion queue entry 2 and completion
queue entry 3 have now been consumed (i.e., completion queue entry 4 is the next completion queue entry
for the host to consume). The controller internal Completion Queue Tail Pointer has not changed.


At time 5, the controller has completed 11 commands and the host has consumed 8 of the completion
queue entries. As a result of the 4 additional commands having been completed, the Phase Tag bit has
been inverted to ‘0’ in completion queue entry 1 through completion queue entry 4. As a result of the 4
additional completion queue entries having been consumed, the host has updated the Completion Queue
Head Pointer to indicate that completion queue entry 5 through completion queue entry 1 (i.e., accounting
for the queue wrap condition) have now been consumed (i.e., completion queue entry 2 is the next
completion queue entry for the host to consume). The controller has updated the internal Completion Queue
Tail Pointer to indicate that completion queue slot 5 is the next completion queue slot into which the
controller posts a completion queue entry.


At time 6, the controller has completed 11 commands and the host has consumed all 11 of the completion
queue entries. As a result of no new command completions, there are no changes to the Phase Tag bit
values. As a result of the 3 additional completion queue entries having been consumed, the host has
updated the Completion Queue Head Pointer to indicate that completion queue entry 2 through completion
queue entry 4 have now been consumed (i.e., completion queue slot 5 is the next completion queue slot
from which the host consumes a completion queue entry). The queue, at this time, is in the Empty condition
(refer to section 3.3.1.4).


**4.3** **Data Pointer Layouts (PRPs and SGLs)**


This section describes the data structures used to describe the layout of data that can be understood by
the controller and the host.


**Physical Region Page Entry and List**


A physical region page (PRP) entry is a pointer to a physical memory page. PRPs are used as a
scatter/gather mechanism for data transfers between the controller and memory. To enable efficient out of
order data transfers between the controller and the host, PRP entries are a fixed size.


The size of the physical memory page is configured by host software in CC.MPS. Figure 109 shows the
layout of a PRP entry that consists of a Page Base Address and an Offset. The size of the Offset field is
determined by the physical memory page size configured in CC.MPS.


**Figure 109: PRP Entry Layout**

|63 n+1|n 0|
|---|---|
|Page Base Address|Offset|



The definition of a PRP entry is described in Figure 110.


149


NVM Express [®] Base Specification, Revision 2.2


**Figure 110: PRP Entry – Page Base Address and Offset**






|Bits|Description|
|---|---|
|63:00|**Page Base Address and Offset (PBAO):**This field indicates the 64-bit physical memory page<br>address. The least significant bits (_n_:0) of this field indicate the offset within the memory page (e.g., if<br>the memory page size is 4 KiB, then bits 11:00 form the Offset; if the memory page size is 8 KiB, then<br>bits 12:00 form the Offset). If this entry is not the first PRP entry in the command or a PRP List pointer<br>in a command, then the Offset portion of this field shall be cleared to 0h. The Offset shall be dword<br>aligned, indicated by bits 1:0 being cleared to 00b.<br>Note: The controller is not required to check that bits 1:0 are cleared to 00b. The controller may report<br>an error of PRP Offset Invalid if bits 1:0 are not cleared to 00b. If the controller does not report an<br>error of PRP Offset Invalid, then the controller shall operate as if bits 1:0 are cleared to 00b.|



A physical region page list (PRP List) is a set of PRP entries in a single page of contiguous memory. A PRP
List describes additional PRP entries that could not be described within the command itself. Any PRP
entries described within the command are not duplicated in a PRP List. If the amount of data to transfer
requires multiple PRP List memory pages, then the last PRP entry before the end of the memory page shall
be a pointer to the next PRP List, indicating the next segment of the PRP List. Figure 111 shows the layout
of a PRP List where each PRP entry identifies memory pages that are physically contiguous. Figure 112
shows the layout of a PRP List where each PRP entry identifies a different memory page (i.e., the memory
pages are not physically contiguous).


**Figure 111: PRP List Layout for Physically Contiguous Memory Pages**

|63 n+1|n 0|
|---|---|
|Page Base Address_p_|0h|
|Page Base Address_p_+1|0h|
|…|…|
|Page Base Address_p+q_|0h|
|Page Base Address_p+q_+1|0h|



**Figure 112: PRP List Layout for Physically Non-Contiguous Memory Pages**

|63 n+1|n 0|
|---|---|
|Page Base Address p|0h|
|Page Base Address q|0h|
|…|…|
|Page Base Address r|0h|
|Page Base Address s|0h|



Dependent on the command definition, the first PRP entry contained within the command may have a nonzero offset within the memory page. The first PRP List entry (i.e., the first pointer to a memory page
containing additional PRP entries) that if present is typically contained in the PRP Entry 2 location within
the command, shall be qword aligned and may also have a non-zero offset within the memory page.


PRP entries contained within a PRP List shall have a memory page offset of 0h. If a second PRP entry is
present within a command, it shall have a memory page offset of 0h. In both cases, the entries are memory
page aligned based on the value in CC.MPS. If the controller receives a non-zero offset for these PRP
entries the controller should return an error of PRP Offset Invalid.


PRP Lists shall be minimally sized with packed entries starting with entry 0. If more PRP List pages are
required, then the last entry of the PRP List contains the Page Base Address of the next PRP List page.
The next PRP List page shall be memory page aligned. The total number of PRP entries required by a
command is implied by the command parameters and memory page size.


150


NVM Express [®] Base Specification, Revision 2.2


**Scatter Gather List (SGL)**


A Scatter Gather List (SGL) is a data structure in memory address space used to describe a data buffer.
The controller indicates the SGL types that the controller supports in the Identify Controller data structure.
A data buffer is either a source buffer or a destination buffer. An SGL contains one or more SGL segments.


The SGL length is the combined total of the values in the Length fields in the SGL Data Block, SGL Bit
Bucket, Keyed SGL Data Block, and Transport SGL Data Block descriptors in an SGL. The SGL length
shall be equal to or exceed the requested data transfer length.


The requested data transfer length is either defined in the specification of a command (e.g., the requested
data transfer length for the Reservation Acquire command is 16 bytes); or is determined based on values
in one or more command specific locations in the SQE (e.g., the requested data transfer length is specified
in the NLB field for a Write command (refer to the NVM Command Set Specification) and is specified in the
NUMDL field and the NUMDU field for a Get Log Page command (refer to section 5.1.12)).


If the requested data transfer length exceeds the SGL length, then:

  - data shall not be transferred to or from locations that are not described by the SGL;

  - if that SGL is a data SGL, then the controller shall abort the command with a status code of Data
SGL Length Invalid; and

  - if that SGL is a metadata SGL, then the controller shall abort the command with a status code of
Metadata SGL Length Invalid.


An SGL segment is a qword aligned data structure in a contiguous region of physical memory describing
all, part of, or none of a data buffer and the next SGL segment, if any. An SGL segment consists of an array
of one or more SGL descriptors. Only the last descriptor in an SGL segment may be an SGL Segment
descriptor or an SGL Last Segment descriptor.


A last SGL segment is an SGL segment that does not contain an SGL Segment descriptor, or an SGL Last
Segment descriptor.


A controller may support byte or dword alignment and granularity of Data Blocks. If a controller supports
only dword alignment and granularity as indicated in the SGL Support field of the Identify Controller data
structure (refer to Figure 313), then the values in the Address and Length fields of all Data Block descriptors
shall have their two least significant bits cleared to 00b. This requirement applies to Data Block descriptors
that indicate data and/or metadata memory regions.


The SGL Descriptor Threshold (SDT) field in the Identify Controller data structure (refer to Figure 313)
indicates the recommended maximum number of SGL descriptors for a command. If the SDT field is set to
a non-zero value, and a command is submitted for which the sum of:


a) the number of SGL Bit Bucket descriptors with non-zero Length field contents; and
b) the number of SGL Data Block descriptors with a non-zero Length field contents,


exceeds the value of the SDT field, then the performance of the controller may be reduced.


The value of the SDT field shall be less than or equal to the value of the Maximum SGL Data Block
Descriptors (MSDBD) field in the Identify Controller data structure (refer to Figure 313 for the definition of
the MSDBD field).


A Keyed SGL Data Block descriptor is a Data Block descriptor that includes a key that is used as part of
the host memory access. The maximum length that may be specified in a Keyed SGL Data Block descriptor
is (16 MiB – 1).


A Transport SGL Data Block descriptor is a Data Block descriptor that specifies a data block that is
transferred by the NVMe Transport using a transfer mechanism and data buffers that are specific to the
NVMe Transport.


The SGL Identifier Descriptor Sub Type field may indicate additional information about a descriptor. As an
example, the Sub Type may indicate that the Address field is an offset rather than an absolute address.
The Sub Type may also indicate NVMe Transport specific information.


151


NVM Express [®] Base Specification, Revision 2.2


The controller shall examine an SGL descriptor for errors before using that SGL descriptor for data transfer.
SGL descriptor error checking may occur in any order and data may be transferred using a valid SGL
descriptor before an SGL descriptor error is detected in another SGL descriptor. The controller is not
required to examine for errors any SGL descriptor that is not used for data transfer.


If the LLDTS bit is cleared to ‘0’ and the length of an SGL is greater than the requested data transfer length,
then:

  - the controller should not abort the command for this reason; and

  - if the controller does abort the command for this reason, then the controller should abort the
command with a status code of:


`o` Data SGL Length Invalid if that SGL is a data SGL; and

`o` Metadata SGL Length Invalid if that SGL is a metadata SGL.


For all SGL descriptors examined for errors by the controller:

  - If the controller detects an error condition listed in Figure 113, then the controller shall abort the
command with the corresponding status code listed in that figure; and

  - If:


`o` an SGL Data Block descriptor, Keyed SGL Data Block descriptor, or a Transport SGL Data
Block descriptor contains Address or Length fields with either of the two least-significant
bits set to 1b; and

`o` the controller supports only dword alignment and granularity as indicated in the SGL
Support field of the Identify Controller data structure (refer to Figure 313),


then the controller should abort the command with a status code of SGL Data Block Granularity
Invalid.


**Figure 113: SGL Validation Error Conditions**









|SGL Validaton Error Condition|Status Code|
|---|---|
|An SGL segment contains:<br>• <br>an SGL Segment descriptor; or<br>• <br>an SGL Last Segment descriptor,<br>in other than the last descriptor in the segment.|Invalid Number of SGL Descriptors|
|A last SGL segment contains an SGL Segment descriptor or an SGL Last<br>Segment descriptor.|Invalid SGL Segment Descriptor|
|An SGL descriptor has:<br>• <br>an unsupported type; or<br>• <br>a combination of type and subtype.|SGL Descriptor Type Invalid|


Figure 114 defines the SGL segment.


**Figure 114: SGL Segment**





|Bytes|Description|
|---|---|
|**SGL Descriptor List**|**SGL Descriptor List**|
|15:00|**SGL Descriptor 0:**This field is the first SGL descriptor.|
|31:16|**SGL Descriptor 1:** This field is the second SGL descriptor.|
|…|…|
|((n*16)+15):(n*16)|**SGL Descriptor n:** This field is the last SGL descriptor.|


An SGL segment contains one or more SGL descriptors. Figure 115 defines the generic SGL descriptor
format.


152


NVM Express [®] Base Specification, Revision 2.2


**Figure 115: Generic SGL Descriptor Format**






|Bytes|Description|
|---|---|
|14:00|**Descriptor Type Specific (DTS):**This field is descriptor type specific.|
|15|**SGL Identifier (SGLID):**The definition of this field is described in the table below.<br>**Bits**<br>**Description**<br>07:04<br>**SGL Descriptor Type (SGLDT):** Refer to Figure 116.<br>03:00<br>**SGL Descriptor Sub Type (SGLDST):** Refer to Figure 117.|


|Bits|Description|
|---|---|
|07:04|**SGL Descriptor Type (SGLDT):** Refer to Figure 116.|
|03:00|**SGL Descriptor Sub Type (SGLDST):** Refer to Figure 117.|



The SGL Descriptor Type field defined in Figure 116 specifies the SGL descriptor type. If the SGL Descriptor
Type field is set to a reserved value or an unsupported value, then the SGL descriptor shall be processed
as having an SGL Descriptor Type error. If the SGL Descriptor Sub Type field is set to a reserved value or
an unsupported value, then the descriptor shall be processed as having an SGL Descriptor Type error.


An SGL descriptor set to all zeroes is an SGL Data Block descriptor with the Address field cleared to 0h
and the Length field cleared to 0h may be used as a NULL descriptor.


**Figure 116: SGL Descriptor Type**

|Value|Descriptor|
|---|---|
|0h|SGL Data Block descriptor|
|1h|SGL Bit Bucket descriptor|
|2h|SGL Segment descriptor|
|3h|SGL Last Segment descriptor|
|4h|Keyed SGL Data Block descriptor|
|5h|Transport SGL Data Block descriptor|
|6h to Eh|Reserved|
|Fh|Vendor specific|



Figure 117 defines the SGL Descriptor Sub Type values and indicates the SGL Descriptor Types to which
each SGL Descriptor Sub Type applies.


**Figure 117: SGL Descriptor Sub Type Values**













|SGL Descriptor<br>Sub Type|SGL Descriptor<br>Types|Sub Type Description|
|---|---|---|
|0h|0h, 2h, 3h, 4h|**Address:**The Address field specifies the starting 64-bit memory byte address<br>of the Data Block, Segment, or Last Segment descriptor.|
|0h|1h|For Type 1h, the Sub Type field shall be cleared to 0h.|
|0h|All other values|Reserved|
|1h|0h, 2h, 3h|**Offset:**The Address field contains an offset from the beginning of the location<br>where data may be transferred. For NVMe over PCIe implementations, this<br>Sub Type is reserved. For NVMe over Fabrics implementations, refer to <br>section 3.3.2.1.3.1.|
|1h|1h|The controller shall abort the command with the status code of SGL Descriptor<br>Type Invalid.|
|1h|4h|The controller shall abort the command with the status code of SGL Descriptor<br>Type Invalid.|
|1h|All other values|Reserved|
|Ah to Fh|All|**NVMe Transport Specific:**The definitions for this range of Sub Types are<br>defined by the binding section for the associated NVMe Transport.|
|All other values|All|Reserved|


The SGL Data Block descriptor, defined in Figure 118, describes a data block.


153


NVM Express [®] Base Specification, Revision 2.2


**Figure 118: SGL Data Block descriptor**














|Bytes|Description|
|---|---|
|07:00|**Address (ADDR):**If the SGL Identifier Descriptor Sub Type field is cleared to 0h in the SGL Identifier<br>field, then this field specifies the starting 64-bit memory byte address of the data block. If the SGL<br>Identifier Descriptor Sub Type field is set to 1h, then this field contains an offset from the beginning<br>of the location where data may be transferred. If the controller requires dword alignment and<br>granularity as indicated in the SGL Support (SGLS) field of the Identify Controller data structure (refer<br>to Figure 313), then the two least significant bits shall be cleared to 00b.<br>If dword alignment and granularity is required, the controller may report an error of Invalid Field in<br>Command if bits 1:0 are not cleared to 00b. If the controller does not report an error of Invalid Field<br>in Command, then the controller shall operate as if bits 1:0 are cleared to 00b.|
|11:08|**Length (LEN):**This field specifies the length in bytes of the data block. This field cleared to 0h<br>specifies that no data is transferred. An SGL Data Block descriptor specifying that no data is<br>transferred is a valid SGL Data Block descriptor. If the controller requires dword alignment and<br>granularity as specified in the SGL Support (SGLS) field the of Identify Controller data structure, then<br>the two least significant bits shall be cleared to 00b.<br>If dword alignment and granularity is required, the controller may report an error of Invalid Field in<br>Command if bits 1:0 are not cleared to 00b. If the controller does not report an error of Invalid Field<br>in Command, then the controller shall operate as if bits 1:0 are cleared to 00b.<br>If the value in the Address field plus the value in this field is greater than 1_00000000_00000000h,<br>then the SGL Data Block descriptor shall be processed as having a Data SGL Length Invalid or<br>Metadata SGL Length Invalid error.|
|14:12|Reserved|
|15|**SGL Identifier (SGLID):**The definition of this field is described in the table below.<br>**Bits** <br>**Description** <br>07:04<br>**SGL Descriptor Type (SGLDT):** 0h as specified in Figure 116.<br>03:00<br>**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|


|Bits|Description|
|---|---|
|07:04|**SGL Descriptor Type (SGLDT):** 0h as specified in Figure 116.|
|03:00|**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|



The SGL Bit Bucket descriptor, defined in Figure 119, is used to ignore parts of source data.


**Figure 119: SGL Bit Bucket descriptor**












|Bytes|Description|
|---|---|
|07:00|Reserved|
|11:08|**Length (LEN):**This field specifies the amount of source data that is discarded. An SGL Bit Bucket<br>descriptor specifying that no source data be discarded (i.e., this field cleared to 0h) is a valid SGL Bit<br>Bucket descriptor.<br>If the SGL Bit Bucket descriptor describes a destination data buffer (e.g., a read from the controller<br>to host memory), then this field specifies the number of bytes of the source data which the controller<br>shall discard (i.e., not transfer to the destination data buffer). <br>If the SGL Bit Bucket descriptor describes a source data buffer (e.g., a write from host memory to the<br>controller), then the Bit Bucket Descriptor shall be treated as if this field were cleared to 0h (i.e., the<br>Bit Bucket Descriptor has no effect).<br>If SGL Bit Bucket descriptors are supported, their length in a destination data buffer shall be included<br>in the specified length of data to be transferred (e.g., their length in a source data buffer is not included<br>in the transfer length specified by the NLB parameter).|
|14:12|Reserved|
|15|**SGL Identifier (SGLID):**The definition of this field is described in the table below.<br>**Bits**<br>**Description**<br>07:04<br>**SGL Descriptor Type (SGLDT):** 1h as specified in Figure 116.<br>03:00<br>**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|


|Bits|Description|
|---|---|
|07:04|**SGL Descriptor Type (SGLDT):** 1h as specified in Figure 116.|
|03:00|**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|



The SGL Segment descriptor, defined in Figure 120, describes the next SGL segment, which is not the last
SGL segment.


154


NVM Express [®] Base Specification, Revision 2.2


**Figure 120: SGL Segment descriptor**












|Bytes|Description|
|---|---|
|07:00|**Address (ADDR):**If the SGL Descriptor Sub Type field is cleared to 0h in the SGL Identifier field,<br>then this field specifies the starting 64-bit memory byte address of the next SGL segment, which is<br>an SGL segment. If the SGL Descriptor Sub Type field is set to 1h in the SGL Identifier field, then<br>this field contains an offset from the beginning of the location where data may be transferred.|
|11:08|**Length (LEN):**This field specifies the length in bytes of the next SGL segment. This field shall be a<br>non-zero value and a multiple of 16.<br>If the value in the Address field plus the value in this field is greater than 1_00000000_00000000h,<br>then the SGL Segment descriptor shall be processed as having a Data SGL Length Invalid or<br>Metadata SGL Length Invalid error.|
|14:12|Reserved|
|15|**SGL Identifier (SGLID):**The definition of this field is described in the table below.<br>**Bits**<br>**Description**<br>07:04<br>**SGL Descriptor Type (SGLDT):** 2h as specified in Figure 116.<br>03:00<br>**SGL Descriptor Sub Type (SGDST):** Valid values are specified in Figure 117.|


|Bits|Description|
|---|---|
|07:04|**SGL Descriptor Type (SGLDT):** 2h as specified in Figure 116.|
|03:00|**SGL Descriptor Sub Type (SGDST):** Valid values are specified in Figure 117.|



The SGL Last Segment descriptor, defined in Figure 121, describes the next and last SGL segment. A last
SGL segment that contains an SGL Segment descriptor or an SGL Last Segment descriptor is processed
as an error.


**Figure 121: SGL Last Segment descriptor**












|Bytes|Description|
|---|---|
|07:00|**Address (ADDR):**If the SGL Identifier Descriptor Sub Type field is cleared to 0h in the SGL Identifier<br>field, then this field specifies the starting 64-bit memory byte address of the next and last SGL<br>segment, which is an SGL segment. If the SGL Identifier Descriptor Sub Type field is set to 1h, then<br>this field contains an offset from the beginning of the location where data may be transferred.|
|11:08|**Length (LEN):**This field specifies the length in bytes of the next and last SGL segment. This field<br>shall be a non-zero value and a multiple of 16.<br>If the value in the Address field plus the value in this field is greater than 1_00000000_00000000h,<br>then the SGL Last Segment descriptor shall be processed as having a Data SGL Length Invalid or<br>Metadata SGL Length Invalid error.|
|14:12|Reserved|
|15|**SGL Identifier (SGLID):**The definition of this field is described in the table below.<br>**Bits**<br>**Description**<br>07:04<br>**SGL Descriptor Type (SGLDT):** 3h as specified in Figure 116.<br>03:00<br>**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|


|Bits|Description|
|---|---|
|07:04|**SGL Descriptor Type (SGLDT):** 3h as specified in Figure 116.|
|03:00|**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|



The Keyed SGL Data Block descriptor, defined in Figure 122, describes a keyed data block.


**Figure 122: Keyed SGL Data Block descriptor**








|Bytes|Description|
|---|---|
|07:00|**Address (ADDR):**This field specifies the starting 64-bit memory byte address of the data block.|
|10:08|**Length (LEN):**This field specifies the length in bytes of the data block. This field cleared to 0h<br>specifies that no data is transferred. An SGL Data Block descriptor specifying that no data is<br>transferred is a valid SGL Data Block descriptor.<br>If the value in the Address field plus the value in this field is greater than 1_00000000_00000000h,<br>then the SGL Data Block descriptor shall be processed as having a Data SGL Length Invalid or<br>Metadata SGL Length Invalid error.|
|14:11|**Key (KEY):**Specifies a 32-bit key that is associated with the data block.|



155


NVM Express [®] Base Specification, Revision 2.2


**Figure 122: Keyed SGL Data Block descriptor**





|Bytes|Description|
|---|---|
|15|**SGL Identifier (SGLID):**The definition of this field is described in the table below.<br>**Bits**<br>**Description**<br>07:04<br>**SGL Descriptor Type (SGLDT):** 4h as specified in Figure 116.<br>03:00<br>**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|


|Bits|Description|
|---|---|
|07:04|**SGL Descriptor Type (SGLDT):** 4h as specified in Figure 116.|
|03:00|**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|


**Figure 123: Transport SGL Data Block descriptor**













|Bytes|Description|
|---|---|
|07:00|Reserved|
|11:08|**Length (LEN):** This field specifies the length in bytes of the data block. This field cleared to 0h<br>specifies that no data is transferred. A Transport SGL Data Block descriptor specifying that no data<br>is transferred is a valid Transport SGL Data Block descriptor. If the controller requires dword<br>alignment and granularity as specified in the SGL Support field of Identify Controller (refer to Figure<br>313), then the two least significant bits shall be cleared to 00b.<br>The data transfer mechanism and data buffers for data specified by a Transport SGL Data Block<br>descriptor are defined by the binding section for the associated NVMe Transport.|
|14:12|Reserved|
|15|**SGL Identifier (SGLID):**The definition of this field is described in the table below.<br>**Bits**<br>**Description**<br>07:04<br>**SGL Descriptor Type (SGLDT):** 5h as specified in Figure 116.<br>03:00<br>**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|


|Bits|Description|
|---|---|
|07:04|**SGL Descriptor Type (SGLDT):** 5h as specified in Figure 116.|
|03:00|**SGL Descriptor Sub Type (SGLDST):** Valid values are specified in Figure 117.|


**SGL Example**



Figure 124 shows an example of a data read request using SGLs. In the example, the logical block size is
512B. The total length of the logical blocks accessed is 13 KiB, of which only 11 KiB is transferred to the
host. The Number of Logical Blocks (NLB) field in the command shall specify 26, indicating the total length
of the logical blocks accessed on the controller is 13 KiB. There are three SGL segments describing the
locations in memory where the logical block data is transferred.


The three SGL segments contain a total of three Data Block descriptors with lengths of 3 KiB, 4 KiB, and
4 KiB respectively. Segment 1 of the Destination SGL contains a Bit Bucket descriptor with a length of 2 KiB
that specifies to not transfer (i.e., ignore) 2 KiB of logical block data from the NVM. Segment 1 of the
destination SGL also contains a Last Segment descriptor specifying that the segment pointed to by the
descriptor is the last SGL segment.


156


NVM Express [®] Base Specification, Revision 2.2


**Figure 124: SGL Read Example**





Bit Bucket data







SGL Data Block descriptor

specifies to transfer 3KiB


Segment descriptor
points to the next memory

location in the SGL


Data Block descriptor
specifies to transfer 4KiB


logical block data


Last Segment descriptor
points to the last memory

location in the SGL


Data Block descriptor
specifies to transfer 4KiB


**Metadata Region (MR)**




|Address = A|Col2|Col3|
|---|---|---|
|0||Length = 3KiB|
|Address = Segment 1<br>2<br>Length = 48|Address = Segment 1<br>2<br>Length = 48|Address = Segment 1<br>2<br>Length = 48|
|2|2|Length = 48|






|1|Col2|Length = 2KiB|
|---|---|---|
|Address = Segment 2|Address = Segment 2|Address = Segment 2|
|3||Length = 16|


|Address = C|Col2|Col3|
|---|---|---|
|0||Length = 4KiB|



The definition for the Metadata Region is command set specific. Refer to each I/O Command Set
specification for applicability and additional details, if any.


**4.4** **Feature Values**


The Get Features command (refer to section 5.1.11) and Set Features command (refer to section 5.1.25)
may be used to read and modify operating parameters of the controller. The operating parameters are
grouped and identified by Feature Identifiers. Each Feature Identifier contains one or more attributes that
may affect the behavior of the Feature.


157


NVM Express [®] Base Specification, Revision 2.2


If the Save and Select Feature Support (SSFS) bit is set to ‘1’ in the Optional NVM Command Support
(ONCS) field of the Identify Controller data structure in Figure 313, then for each Feature, there are three
settings: default, saved, and current. If the SSFS bit is cleared to ‘0’, then the controller only supports a
current and default value for each Feature. In this case, the current value may be persistent across power
cycles and resets based on the information specified in Figure 386.


If the SSFS bit is set to ‘1’, then each Feature has supported capabilities (refer to Figure 196), which are
discovered using the Supported Capabilities value in the Select field in Get Features (refer to Figure 193).


The default value for each Feature is vendor specific and set by the manufacturer unless otherwise
specified. The default value is not changeable.


The current value for a Feature is the value in active use by the controller for that Feature.


A Set Features command uses the value specified by the command to set:


a) the current value for that Feature; or
b) the current value for that Feature and the saved value for that Feature, if that Feature is saveable.


A Feature may be saveable. If a Feature is saveable (i.e., the controller supports the Save field in the Set
Features command and the Select field in the Get Features command), then any Feature Identifier that is
namespace specific may be saved on a per namespace basis.


If a Feature is not saveable, or does not have a saved value, then a Get Features command to read the
saved value returns the default value.


If a Feature is not saveable and is persistent as specified in Figure 386, then the current value of that
Feature shall be persistent across power cycles and resets.


The current value for a Feature, as a result of a Controller Level Reset, is indicated in Figure 125 for an
NVM subsystem that supports only a single controller (i.e., the Multiple Ports bit of the CMIC field (refer to
Figure 312) is cleared to ‘0’).


The current value for a Feature, as a result of an NVM Subsystem Reset, is indicated in Figure 125, for an
NVM subsystem:

  - that is able to support two or more controllers and does not support multiple domains; or

  - supports multiple domains where the NVM Subsystem Reset results in a reset of the entire NVM
subsystem.


**Figure 125: Current Value after Reset with Scope of Entire NVM Subsystem**






















|Feature<br>Capability|Controller scope or<br>Namespace per<br>controller scope|NVM subsystem<br>scope|Endurance Group<br>scope|NVM Set<br>scope|Namespace<br>scope|
|---|---|---|---|---|---|
|Saveable|Set to:<br>• <br>the saved value if a saved value is set; or<br>• <br>the default value if a saved value is not set,<br>unless otherwise specified.|Set to:<br>• <br>the saved value if a saved value is set; or<br>• <br>the default value if a saved value is not set,<br>unless otherwise specified.|Set to:<br>• <br>the saved value if a saved value is set; or<br>• <br>the default value if a saved value is not set,<br>unless otherwise specified.|Set to:<br>• <br>the saved value if a saved value is set; or<br>• <br>the default value if a saved value is not set,<br>unless otherwise specified.|Set to:<br>• <br>the saved value if a saved value is set; or<br>• <br>the default value if a saved value is not set,<br>unless otherwise specified.|
|Non-saveable<br>and non-<br>persistent|Set to the default value, unless otherwise specified.|Set to the default value, unless otherwise specified.|Set to the default value, unless otherwise specified.|Set to the default value, unless otherwise specified.|Set to the default value, unless otherwise specified.|



The current value for a Feature, as a result of a Controller Level Reset, is indicated in Figure 126 for an
NVM subsystem that is able to support two or more controllers (i.e., the Multiple Ports bit is set to ‘1’ in the
CMIC field).


The current value for a Feature, as a result of an NVM Subsystem Reset, is indicated in Figure 126 for an
NVM subsystem that supports:

  - multiple domains where an NVM Subsystem Reset does not reset the entire NVM subsystem as
defined in section 3.7.1.2.


158


NVM Express [®] Base Specification, Revision 2.2


**Figure 126: Current Value after Reset with Scope of Subset of the NVM Subsystem**
















|Feature<br>Capability|Controller scope or Namespace<br>per controller scope|NVM<br>subsystem<br>scope|Endurance<br>Group scope|NVM<br>Set<br>scope|Namespace<br>scope|
|---|---|---|---|---|---|
|Saveable|Set to:<br>• the saved value if a saved value<br>is set; or<br>• the default value if a saved<br>value is not set,<br>unless otherwise specified.|Unchanged, unless otherwise specified.|Unchanged, unless otherwise specified.|Unchanged, unless otherwise specified.|Unchanged, unless otherwise specified.|
|Non-saveable<br>and non-<br>persistent|Set to the default value, unless<br>otherwise specified.|Set to the default value, unless<br>otherwise specified.|Set to the default value, unless<br>otherwise specified.|Set to the default value, unless<br>otherwise specified.|Set to the default value, unless<br>otherwise specified.|



Concurrent access to Feature values by multiple hosts, for features with a scope other than controller
scope, requires some form of coordination between hosts. The procedure used to coordinate these hosts
is outside the scope of this specification.


Feature settings apply based on the feature scope (e.g., a feature is namespace specific if that feature has
a namespace scope) as defined in Figure 386.


For feature values that apply to the controller scope:


a) if the NSID field is cleared to 0h or set to FFFFFFFFh, then:

    - the Set Features command shall set the specified feature value for the controller; and

    - the Get Features command shall return the current setting of the requested feature value for
the controller;


and


b) if the NSID field is set to a valid namespace identifier (refer to section 3.2.1.2), then:

    - the Set Features command shall abort with a status code of Feature Not Namespace Specific;
and

    - the Get Features command shall return the current setting of the requested feature value for
the controller.


For feature values that apply to the namespace scope:


a) if the NSID field is set to an active namespace identifier (refer to section 3.2.1.4), then:

    - the Set Features command shall set the specified feature value of the specified namespace;
and

    - the Get Features command shall return the current setting of the requested feature value for
the specified namespace;


b) if the NSID field is set to FFFFFFFFh, then:

    - for the Set Features command, the controller shall:


`o` if the MDS bit is set to ‘1’ in the Identify Controller data structure, abort the command with
a status code of Invalid Field in Command; or

`o` if the MDS bit is cleared to ‘0’ in the Identify Controller data structure, unless otherwise
specified, set the specified feature value for all namespaces attached to the controller
processing the command;


and


    - for the Get Features command, the controller shall, unless otherwise specified in section
5.1.25, abort the command with a status code of Invalid Namespace or Format;


159


NVM Express [®] Base Specification, Revision 2.2


and


c) if the NSID field is set to any other value, then the Set Features command and the Get Features

command is aborted by the controller as described in Figure 92.


For feature values that apply to NVM subsystem scope, Domain scope, NVM Set scope, or Endurance
Group scope:


a) the NSID field should be cleared to 0h; and
b) if the NSID field is set to a non-zero value, then the Set Features command and the Get Features

command are aborted by the controller as described in Figure 92.


There are mandatory and optional Feature Identifiers defined in section 3.1.3.6. If a Get Features command
or Set Features command is processed that specifies a Feature Identifier that is not supported, then the
controller shall abort the command with a status code of Invalid Field in Command.


**4.5** **Identifier Format and Layout (Informative)**


This section provides guidance for proper implementation of various identifiers defined in the Identify
Controller, Identify Namespace, and Namespace Identification Descriptor data structures.


**PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)**


The PCI Vendor ID (VID, bytes 01:00) and PCI Subsystem Vendor ID (SSVID, bytes 03:02) are defined in
the Identify Controller data structure. The values are assigned by the PCI SIG. Each identifier is a 16-bit
number in little endian format.


Example:

  - VID = ABCDh; and

  - SSVID = 1234h.


**Figure 127: PCI Vendor ID (VID) and PCI Subsystem Vendor ID (SSVID)**

|Bytes|00|01|02|03|
|---|---|---|---|---|
|**Value**|CDh|ABh|34h|12h|



**Serial Number (SN) and Model Number (MN)**


The Serial Number (SN, bytes 23:04) and Model Number (MN, bytes 63:24) are defined in the Identify
Controller data structure. The values are ASCII strings assigned by the vendor. Each identifier is in big
endian format.


Example (Value shown as ASCII characters):

  - SN = “SN1”; and

  - MN = “M2”.


**Figure 128: Serial Number (SN) and Model Number (MN)**

|Bytes|04|05|06|23 to 07|24|25|63 to 26|
|---|---|---|---|---|---|---|---|
|**Value**|53h (‘S’)|4Eh (‘N’)|31h (‘1’)|20h (‘ ‘)|4Dh (‘M’)|32h (‘2’)|20h (‘ ‘)|



**IEEE OUI Identifier (IEEE)**


The IEEE OUI Identifier (OUI, bytes 75:73) is defined in the Identify Controller data structure. The value is
assigned by the IEEE Registration Authority. The identifier is in little endian format.


Example:

  - OUI = ABCDEFh.


160


NVM Express [®] Base Specification, Revision 2.2


**Figure 129: IEEE OUI Identifier (IEEE)**

|Bytes|73|74|75|
|---|---|---|---|
|**Value**|EFh|CDh|ABh|



**IEEE Extended Unique Identifier (EUI64)**


The IEEE Extended Unique Identifier (EUI64, bytes 127:120) is defined in the Identify Namespace data
[structure. Tutorials are available at https://standards.ieee.org/develop/regauth/tut/index.html. IEEE defines](https://standards.ieee.org/develop/regauth/tut/index.html)
three formats that may be used in this field: MA-L, MA-M, and MA-S. The examples in this section use the
MA-L format.


The MA-L format is defined as a string of eight octets:


**Figure 130: IEEE Extended Unique Identifier (EUI64), MA-L Format**

|EUI[0]|EUI[1]|EUI[2]|EUI[3]|EUI[4]|EUI[5]|EUI[6]|EUI[7]|
|---|---|---|---|---|---|---|---|
|OUI|OUI|OUI|Extension Identifier|Extension Identifier|Extension Identifier|Extension Identifier|Extension Identifier|



EUI64 is defined in big endian format. The OUI field differs from the OUI Identifier which is in little endian
format as described in section 4.5.3.


Example:

  - OUI Identifier = ABCDEFh; and

  - Extension Identifier = 0123456789h.


**Figure 131: IEEE Extended Unique Identifier (EUI64), OUI Identifier**

|Bytes|120|121|122|123|124|125|
|---|---|---|---|---|---|---|
|**Value**|ABh|CDh|EFh|01h|23h|45h|
|**Field**|OUI|OUI|OUI|Extension Identifier|Extension Identifier|Extension Identifier|



**Figure 132: IEEE Extended Unique Identifier (EUI64), Ext. ID (cont)**

|Bytes|126|127|
|---|---|---|
|**Value**|67h|89h|
|**Field**|Ext ID (cont)|Ext ID (cont)|



The MA-L format is similar to the World Wide Name (WWN) format defined as IEEE Registered designator
(NAA = 5) as shown below.


**Figure 133: MA-L similarity to WWN**

|Bytes|0|Col3|1|2|3|Col7|4|5|6|7|
|---|---|---|---|---|---|---|---|---|---|---|
|**EUI64**|OUI|OUI|OUI|OUI|Extension Identifier|Extension Identifier|Extension Identifier|Extension Identifier|Extension Identifier|Extension Identifier|
|**WWN**<br>**(NAA = 5)**|5h|OUI|OUI|OUI|OUI|Vendor Specific Identifier|Vendor Specific Identifier|Vendor Specific Identifier|Vendor Specific Identifier|Vendor Specific Identifier|



**Namespace Globally Unique Identifier (NGUID)**


The Namespace Globally Unique Identifier (NGUID, bytes 119:104) is defined in the Identify Namespace
data structure. The NGUID is composed of an IEEE OUI, an extension identifier, and a vendor specific
extension identifier. The extension identifier and vendor specific extension identifier are both assigned by
the vendor and may be considered as a single field. NGUID is defined in big endian format. The OUI field
differs from the OUI Identifier which is in little endian format as described in section 4.5.3.


161


NVM Express [®] Base Specification, Revision 2.2


Example:

  - OUI Identifier = ABCDEFh;

  - Extension Identifier = 0123456789h; and

  - Vendor Specific Extension Identifier = FEDCBA9876543210h.


**Figure 134: Namespace Globally Unique Identifier (NGUID)**

|Bytes|104|105|106|107|108|109|
|---|---|---|---|---|---|---|
|**Value**|FEh|DCh|BAh|98h|76h|54h|
|**Field**|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|



**Figure 135: Namespace Globally Unique Identifier (NGUID), OUI**

|Bytes|110|111|112|113|114|115|
|---|---|---|---|---|---|---|
|**Value**|32h|10h|ABh|CDh|EFh|01h|
|**Field**|VSP Ex ID (cont)|VSP Ex ID (cont)|OUI|OUI|OUI|Ex ID|



**Figure 136: Namespace Globally Unique Identifier**

**(NGUID), Extension Identifier (continued)**

|Bytes|116|117|118|119|
|---|---|---|---|---|
|**Value**|23h|45h|67h|89h|
|**Field**|Extension Identifier (continued)|Extension Identifier (continued)|Extension Identifier (continued)|Extension Identifier (continued)|



The NGUID format is similar to the World Wide Name (WWN) format as IEEE Registered Extended
designator (NAA = 6) as shown below.


**Figure 137: Namespace Globally Unique Identifier (NGUID), NGUID similarity to WWN**

|Bytes|0|Col3|1|2|3|Col7|4|5|6|7|8|9|10|11|12|13|14|15|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**NGUID**|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|Vendor Specific Extension Identifier|OUI|OUI|OUI|Extension Identifier|Extension Identifier|Extension Identifier|Extension Identifier|Extension Identifier|
|**WWN**<br>**(NAA = 6)**|6h|<br>OUI|<br>OUI|<br>OUI|<br>OUI|Vendor Specific Identifier|Vendor Specific Identifier|Vendor Specific Identifier|Vendor Specific Identifier|Vendor Specific Identifier|<br>Vendor Specific Identifier Extension|<br>Vendor Specific Identifier Extension|<br>Vendor Specific Identifier Extension|<br>Vendor Specific Identifier Extension|<br>Vendor Specific Identifier Extension|<br>Vendor Specific Identifier Extension|<br>Vendor Specific Identifier Extension|<br>Vendor Specific Identifier Extension|



**Universally Unique Identifier (UUID)**


The Universally Unique Identifier is defined in RFC 9562 and contained in the Namespace Identification
Descriptor (refer to Figure 316). Byte ordering requirements for a UUID are described in RFC 9562.


For historical reasons, UUID subtypes are called UUID versions. Multiple UUID versions are able to be
used in the same implementation.


RFC 9562 defines UUID version 8 (i.e., UUIDv8) for experimental or vendor-specific use cases. Uniqueness
of UUIDv8 values is implementation specific. NVM Express UUID use cases assume uniqueness within the
set of hosts, NVM subsystems, and fabrics that are connected or accessible by a common instance of an
administrative tool. For UUIDv8 values, that uniqueness is the responsibility of all of the implementations
in that set. RFC 9562 Appendix B provides examples of UUIDv8 generation algorithms that produce unique
UUIDs if all implementations in that set generate UUIDv8 values with the same algorithm.


**4.6** **List Data Structures**


This section describes list data structures used in this specification.


**Controller List**


A Controller List, defined in Figure 138, is an ordered list of ascending controller identifiers. The controller
identifier of a controller is the value indicated in the CNTLID field of the Identify Controller data structure in
Figure 313. Unused entries are zero filled.


162


NVM Express [®] Base Specification, Revision 2.2


**Figure 138: Controller List Format**














|Bytes|Description|
|---|---|
|**Header**|**Header**|
|01:00|**Number of Controller Identifiers (NUMCIDS):**This field contains the number of controller<br>entries in the list. There may be up to 2,047 identifiers in the list. A value of 0h indicates there<br>are no controllers in the list.|
|**Controller Identifier List**|**Controller Identifier List**|
|03:02|**Controller Identifier 0:**This field contains the NVM subsystem unique controller identifier for<br>the first controller in the list, if present.|
|05:04|**Controller Identifier 1:**This field contains the NVM subsystem unique controller identifier for<br>the second controller in the list, if present.|
|…|…|
|(NUMCIDS*2+1):<br>(NUMCIDS*2)|**Controller Identifier NUMCIDS-1:**This field contains the NVM subsystem unique controller<br>identifier for the last controller in the list, if present.|



**Namespace List**


A Namespace List, defined in Figure 139, is an ordered list of namespace IDs. Unused entries are zero
filled.


**Figure 139: Namespace List Format**

|Bytes|Description|
|---|---|
|**Namespace Identifier List**|**Namespace Identifier List**|
|03:00|**Namespace Identifier 0:**This field contains the lowest namespace ID in the list or 0h if the list is<br>empty.|
|07:04|**Namespace Identifier 1:**This field contains the second lowest namespace ID in the list or 0h if the<br>list contains less than two entries.|
|…|…|
|(N*4+3):(N*4)|**Namespace Identifier N:**This field contains the largest namespace ID in the list or 0h if the list<br>contains less than N+1 entries.|



**4.7** **NVMe Qualified Names**


NVMe Qualified Names (NQNs) are used to uniquely describe a host or NVM subsystem for the purposes
of identification and authentication. The NVMe Qualified Name for the NVM subsystem is specified in the
Identify Controller data structure. An NQN is permanent for the lifetime of the host or NVM subsystem.


An NVMe Qualified Name is encoded as a UTF-8 string of Unicode characters (refer to section 1.4.2) with
the following properties:

  - The encoding is UTF-8 (refer to RFC 3629);

  - The following characters are used in formatting:


`o` dash (‘-‘=U+002d);

`o` dot (‘.’=U+002e); and

`o` colon (‘:’=U+003a);

  - The maximum name is 223 bytes in length; and

  - The string is null terminated.


There are two supported NQN formats. The first format may be used by any organization that owns a
domain name. This naming format may be used to create a human interpretable string to describe the host
or NVM subsystem. This format consists of:

  - The string “nqn”;

  - The string “.” (i.e., the ASCII period character);


163


NVM Express [®] Base Specification, Revision 2.2


  - A date code, in “yyyy-mm” format. This date shall be during a time interval when the naming
authority owned the domain name used in this format. The date code uses the Gregorian calendar.
All digits and the dash shall be included;

  - The string “.” (i.e., the ASCII period character);

  - The reverse domain name of the naming authority that is creating the NQN; and

  - A colon (:) prefixed string that the owner of the domain name assigns that does not exceed the
maximum length. The naming authority is responsible to ensure that the NQN is worldwide unique.


The reverse domain name in an NQN that uses this format shall not be “org.nvmexpress”.


The following are examples of NVMe Qualified Names that may be generated by “Example NVMe, Inc.”

  - The string “nqn.2014-08.com.example:nvme:nvm-subsystem-sn-d78432”; and

  - The string “nqn.2014-08.com.example:nvme.host.sys.xyz”.


The second format may be used to create a unique identifier when there is not a naming authority or there
is not a requirement for a human interpretable string. This format consists of:

  - The string “nqn”;

  - The string “.” (i.e., the ASCII period character);

  - The string “2014-08.org.nvmexpress:uuid:”; and

  - A 128-bit UUID based on the definition in RFC 9562 represented as a string formatted as
“ _11111111-2222-3333-4444-555555555555”_ .


The following is an example of an NVMe Qualified Name using the UUID-based format:

  - The string “nqn.2014-08.org.nvmexpress:uuid:f81d4fae-7dec-11d0-a765-00a0c91e6bf6”.


NVMe hosts, controllers and NVM subsystems process (e.g., compare for equality) UTF-8 NVMe Qualified
Names without any text processing or text comparison logic that is specific to the Unicode character set or
locale (refer to section 4.8).


**Unique Identifier**


**Unique Identifier Overview**


Unique identifiers include the following:


a) NVM subsystem unique identifiers (refer to section 4.7.1.2);
b) controller unique identifiers (refer to section 4.7.1.3); and
c) namespace unique identifiers (refer to section 4.7.1.4).


Unique identifiers are either globally unique or unique only within the NVM subsystem. NVM subsystem
unique identifiers are globally unique. Controller unique identifiers (i.e., the CNTLID) are unique only within
the NVM subsystem. Namespace unique identifiers are globally unique.


**NVM Subsystem Unique Identifier**


The NVM Subsystem NVMe Qualified Name specified in the Identify Controller data structure (refer to
Figure 313) should be used (e.g., by host software) as the unique identifier for the NVM subsystem. If the
controller is compliant with an NVM Express Specification prior to revision 1.2.1 (i.e., revisions where the
NVM Subsystem NQN was not defined), then the PCI Vendor ID, Serial Number, and Model Number fields
in the Identify Controller data structure and the NQN Starting String “nqn.2014.08.org.nvmexpress:” may
be combined by the host to form a globally unique value that identifies the NVM subsystem (e.g., for host
software that uses NQNs). The method shown in Figure 140 should be used by the host to construct an
NVM Subsystem NQN for older NVM subsystems that do not provide an NQN in the Identify Controller data
structure. The mechanism used by the vendor to assign Serial Number and Model Number values to ensure
uniqueness is outside the scope of this specification.


164


NVM Express [®] Base Specification, Revision 2.2


**Figure 140: NQN Construction for Older NVM Subsystems**

|Bytes|Description|
|---|---|
|26:00|**NQN Starting String (NSS):**Contains the 27 letter ASCII string ”nqn.2014-08.org.nvmexpress:”.|
|30:27|**PCI Vendor ID (VID):**Contains the company vendor identifier that is assigned by the PCI SIG as a<br>hexadecimal ASCII string.|
|34:31|**PCI Subsystem Vendor ID (SSVID):**Contains the company vendor identifier that is assigned by the<br>PCI SIG for the subsystem as a hexadecimal ASCII string.|
|54:35|**Serial Number (SN):** Contains the serial number for the NVM subsystem that is assigned by the vendor<br>as an ASCII string.|
|94:55|**Model Number (MN):**Contains the model number for the NVM subsystem that is assigned by the<br>vendor as an ASCII string.|
|222:95|**Padding (PAD):**Contains spaces (ASCII character 20h).|



**Controller Unique Identifier**


An NVM subsystem may contain multiple controllers. All controllers contained in the NVM subsystem share
the same NVM subsystem unique identifier. The Controller ID (CNTLID) value returned in the Identify
Controller data structure may be used to uniquely identify a controller within an NVM subsystem. The
Controller ID value when combined with the NVM subsystem identifier forms a globally unique value that
identifies the controller. The mechanism used by the vendor to assign Controller ID values is outside the
scope of this specification.


**Namespace Unique Identifier**


The Identify Namespace data structure (refer to the applicable I/O Command Set specification) contains
the IEEE Extended Unique Identifier (EUI64) and the Namespace Globally Unique Identifier (NGUID) fields.
The Namespace Identification Descriptor data structure (refer to Figure 316) contains the Namespace
UUID. EUI64 is an 8-byte EUI-64 identifier (refer to section 4.5.4), NGUID is a 16-byte identifier based on
EUI-64 (refer to section 4.5.5), and Namespace UUID is a 16-byte identifier described in RFC 9562 (refer
to section 4.5.6).


When creating a namespace, the controller shall indicate a globally unique namespace identifier in one or
more of the following:


a) the EUI64 field;
b) the NGUID field; or
c) a Namespace Identification Descriptor with the Namespace Identifier Type field set to 3h (i.e., a

UUID).


Refer to section 8.1.9.2 for additional globally unique namespace identifier requirements related to
dispersed namespaces.


If the EUI64 field is cleared to 0h and the NGUID field is cleared to 0h, then the namespace shall support
a valid Namespace UUID in the Namespace Identification Descriptor data structure.


If the UIDREUSE bit in the NSFEAT field is cleared to ‘0’, then a controller may reuse a non-zero
NGUID/EUI64 value for a new namespace after the original namespace using the value has been deleted.
If the UIDREUSE bit is set to ‘1’, then a controller shall not reuse a non-zero NGUID/EUI64 for a new
namespace after the original namespace using the value has been deleted.


**4.8** **UTF-8 String Processing**


NVMe hosts, controllers and NVM subsystems process (e.g., store, compare) UTF-8 strings used by NVMe
as binary strings without any text processing or text comparison logic that is specific to the Unicode
character set or locale (e.g., check for byte values not used by UTF-8, Unicode normalization, etc.). Any
such text processing:


a) may occur as part of entry of UTF-8 strings into NVMe hosts and NVM subsystems as shown at

points 1 and 3 in Figure 141; and


165


NVM Express [®] Base Specification, Revision 2.2


b) should not occur as part of receiving UTF-8 strings via NVMe, as shown at points 2 and 4 in Figure

141.


Upon entry into the NVMe host (e.g., via a configuration interface at point 1 in Figure 141, described as
“input” in RFC 9562), NVMe host software may process a UTF-8 string (e.g., perform Unicode
normalization). Upon entry into the NVM subsystem (e.g., via a configuration interface at point 3 in Figure
141, described as “input” in RFC 9562), a controller may process a UTF-8 string (e.g., perform Unicode
normalization). Upon receipt by the host (e.g., at point 2 in Figure 141) of a UTF-8 string from the controller,
text processing (e.g., Unicode normalization) should not occur. Upon receipt by the controller (e.g., at point
4 in Figure 141) of a UTF-8 string from the host, text processing (e.g., Unicode normalization) should not
occur.


**Figure 141: UTF-8 Input Processing**

### Host NVM subsystem



UTF-8 Entry UTF-8 Entry















166


