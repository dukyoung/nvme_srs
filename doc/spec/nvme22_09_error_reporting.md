NVM Express [®] Base Specification, Revision 2.2


**9 Error Reporting and Recovery**


**9.1** **Command and Queue Error Handling**


In the case of serious error conditions, like Completion Queue Invalid, the operation of the associated
Submission Queue or Completion Queue may be compromised. In this case, host software should delete
the associated Completion Queue and/or Submission Queue. The delete of a Submission Queue aborts all
outstanding commands, and deletion of either queue type releases resources associated with that queue.
Host software should recreate the Completion Queue and/or Submission Queue to then continue with
operation.


In the case of serious error conditions for Admin commands, the entire controller should be reset using a
Controller Level Reset. The entire controller should also be reset if a completion is not received for the
deletion of a Submission Queue or Completion Queue.


For most command errors, there is not an issue with the Submission Queue and/or Completion Queue
itself. Thus, host software and the controller should continue to process commands. It is at the discretion
of host software whether to retry the failed command; the Retry bit in the completion queue entry indicates
whether a retry of the failed command may succeed.


**9.2** **Media and Data Error Handling**


In the event that the requested operation could not be performed to the NVM media, the particular command
is completed with a media error indicating the type of failure using the appropriate status code.


If a read error occurs during the processing of a command, (e.g., End-to-end Guard Check Error,
Unrecovered Read Error), the controller may either stop the DMA transfer into the memory or transfer the
erroneous data to the memory. The host shall ignore the data in the memory locations for commands that
complete with such error conditions.


If a write error occurs during the processing of a command, (e.g., an internal error, End-to-end Guard Check
Error, End-to-end Application Tag Check Error), the controller may either stop or complete the DMA
transfer.


Additional I/O Command Set specific error handling is described within applicable I/O Command Set
specifications.


**9.3** **Memory Error Handling**


For PCI Express implementations, memory errors such as target abort, master abort, and parity may cause
the controller to stop processing the currently executing command. These are serious errors that cannot be
recovered from without host software intervention.


A master abort or target abort error occurs when host software has provided, to the controller, the address
of memory that does not exist. When this occurs, the controller aborts the command with a Data Transfer
Error status code.


**9.4** **Internal Controller Error Handling**


If a controller level failure (e.g., a DRAM failure) occurs during the processing of a command, then the
controller should abort the command with a status code of Internal Error. Any data transfer associated with
the command may be incomplete or incorrect, and therefore any transferred data should not be used for
any purpose other than error reporting or diagnosis. The host may choose to re-submit the command or
indicate an error to the higher-level software.


**9.5** **Controller Fatal Status Condition**


If the controller has a serious error condition and is unable to communicate with host software via
completion queue entries in the Admin Completion Queue or I/O Completion Queues, then the controller
may set the Controller Fatal Status (CSTS.CFS) bit to ‘1’ (refer to section 3.1.4.6). This indicates to host


663


NVM Express [®] Base Specification, Revision 2.2


software that a serious error condition has occurred. When this condition occurs, host software should
attempt to reset and then re-initialize the controller.


The Controller Fatal Status condition is not indicated with an interrupt. If host software experiences timeout
conditions and/or repeated errors, then host software should consult the Controller Fatal Status
(CSTS.CFS) bit to determine if a more serious error has occurred.


If the Controller Fatal Status (CSTS.CFS) bit is set to ‘1’ on any controller in the NVM subsystem, the host
should issue a Controller Reset to that controller.


If that Controller Reset does not clear the Controller Fatal Status condition, the host should initiate an NVM
Subsystem Reset (refer to section 3.7.1), if supported.


Performing an NVM Subsystem Reset (NSSR) may cause PCI Express links to go down as part of resetting
the NVM subsystem. Host software may have undesirable effects related to PCI Express links going down
(e.g., some host operating systems or hypervisors may crash).


NVM Subsystem Reset should not be used if the host software has undesirable effects related to PCI
Express links going down. This host software includes, but is not limited to, operating systems using
Firmware First Error Handling (refer to the ACPI Specification). Such operating systems should not use
NSSR for recovery from CFS conditions.


**9.6** **Communication Loss Handling**


If the host loses communication with a controller, then the host is unable to receive a completion (CQE) for
any outstanding command that has been submitted to that controller (refer to section 3.4.5). If the host is
able to use another controller to access the same NVM subsystem or re-establish communication with the
original controller, then it is strongly recommended that any host use of that controller to recover from
communication loss follow the procedures and requirements in this section in order to avoid possible
corruption of user data and unintended changes to NVM subsystem state.


Host recovery from communication loss with a controller consists of three functional components:

  - Host determination that communication with a controller has been lost is described in section 9.6.1.

  - Host determination that no further processing of outstanding commands is possible on that
controller is described in section 9.6.2.

  - Host retry, if any, of outstanding commands after communication loss is described in section 9.6.3.


These functional components interact with each other. Host detection of communication loss is necessary
before the host is able to determine when no further controller processing of outstanding commands is
possible. Host retries of outstanding commands that modify user data or NVM subsystem state are able to
corrupt user data or make unintended changes to NVM subsystem state unless the host determines that
no further controller processing of the original commands is possible as described in section 9.6.2.


**Host Communication Loss with a Controller**


A host determines that communication has been lost with a controller if:

  - the host detects a Keep Alive Timeout (refer to section 3.9);

  - for message-based transports, the host or the controller terminates the NVMe Transport connection
on which the command was sent (refer to section 3.3.2.4); or

  - the host detects a transport connection loss using methods outside the scope of this specification
(e.g., the transport notifies the host of a loss of communication either with the controller to which
the command was submitted or with the queue on which the command was sent).


A controller may detect a loss of communication at a different time (e.g., later) than the host detects that
loss of communication. As explained in section 9.6.2, additional time may be required for the controller to
stop processing commands after the controller detects a loss of communication.


664


NVM Express [®] Base Specification, Revision 2.2


**End of Controller Processing of Outstanding Commands**


This section describes how a host determines that no further controller processing of an outstanding
command is possible after a loss of communication happens. At the time when a host detects a
communication loss with a controller, the outstanding commands, if any, are commands for which the host
is unable to receive a CQE as a result of the communication loss (refer to section 3.4.5).


Some commands (e.g., Sanitize) initiate background operations. These background operations are able to
continue after a host loss of communication with the controller that started the background operation. After
such a loss of communication, additional measures (e.g., commands submitted to a different controller) are
necessary for the host to track progress and completion of such a background operation.


A host that is unable to communicate with a controller should perform the following steps in order to
determine that no further controller processing of outstanding commands is able to occur:


1. For message-based transports, terminate the association and the associated transport

connections. This step is skipped for memory-based transports.
2. Wait for sufficient time to ensure that the controller has detected a loss of communication using at

least one of the following:


a. If the controller uses Command Based Keep Alive (refer to section 3.9.3.1), wait at least

until 2 * KATT (refer to section 3.9) from the time the host submitted the most recent Keep
Alive Command to the controller;
b. If the controller uses Traffic Based Keep Alive (refer to section 3.9.4.1), wait at least until

3 * KATT from the time the host submitted the most recent command to the controller; or
c. Receive a transport-specific notification for determining that the controller has terminated

an NVMe Transport connection or detected a loss of communication (e.g., a fabric
notification or a PCIe surprise link down error notification for a PCIe link that directly
connects a host to an NVM subsystem (e.g., an SSD)).


3. Wait for additional sufficient time to ensure that the controller has stopped processing commands

using one of the following:


a. If the CQT field (refer to Figure 313) is non-zero, wait for the amount of time indicated in

the CQT field to elapse; or
b. If the CQT field is cleared to 0h, wait for an implementation specific amount of time (e.g.,

10 seconds). The host should allow this value to be administratively configured.


The specification of the times to wait to ensure that the controller has detected a Keep Alive Timeout
described in this section (i.e., 2 * KATT and 3 * KATT) assumes that the transport delays any command by
at most one KATT. Once the last command is fetched by the controller, the controller is required to detect
a Keep Alive Timeout after at most a further 1 * KATT for Command Based Keep Alive and at most 2 *
KATT for Traffic Based Keep Alive (refer to Figure 90). The sum of the two delays (i.e., the transport delay
and the delay to detect the Keep Alive timeout) is 2 * KATT for Command Based Keep Alive and 3 * KATT
for Traffic Based Keep Alive.


**Command Retry After Communication Loss**


If the host loses communication with a controller, then the host is unable to receive a completion (CQE) for
any outstanding command (refer to section 3.4.5) that has been submitted to that controller. If the host is
able to use another controller to access the same NVM subsystem or re-establish communication with the
original controller, the host may be able to use that controller to recover from the communication loss by
retrying outstanding commands. It is strongly recommended that any host retry of any outstanding
commands after communication loss follow the procedures and requirements in this section in order to
avoid possible corruption of user data and unintended changes to NVM subsystem state (e.g., Reservation
state (refer to section 8.1.22)).


For command retry purposes, every outstanding command falls into one of three command retry categories,
Unrestricted Retry, Delayed Retry, or State-Dependent Retry, based on whether the command is
idempotent (refer to section 9.6.3.1), and whether the command modifies user data or NVM subsystem


665


NVM Express [®] Base Specification, Revision 2.2


state. Section 9.6.3.2 defines these categories and describes requirements and restrictions on retrying
outstanding commands in each category.


**Idempotent Commands**


Controller processing of an idempotent command produces the same end state on the NVM subsystem
and returns the same results if that command is resubmitted one or more times with no intervening
commands. All commands tend to modify some ancillary state on the controller (e.g., tracking statistics);
these ancillary changes to state do not prevent a command from being considered idempotent. The results
of the command include the status code (excluding transient status codes or error conditions, e.g., due to
a loss of communication), any data returned to the host and any NVM subsystem changes to user data or
state (e.g., reservation state, feature contents).


For example, a read command addressed to a specific location (e.g., LBA) in a namespace is an idempotent
command. The read command addressed to a valid location in a namespace returns the same data with a
successful completion status code if that command is submitted repeatedly. Similarly, a write command
addressed to a valid location in a namespace writes the same data to that location if submitted repeatedly.
This command is also an idempotent command.


On the other hand, a Namespace Management command (refer to section 5.1.21) that creates a
namespace is not idempotent (i.e., is a non-idempotent command), as repeating the Namespace
Management command creates additional namespaces with different namespace identifiers. Similarly, a
Reservation Register command that unregisters a host (refer to section 7.6) is also not idempotent because
repeating the command attempts to unregister a host that is no longer registered and returns an error status
code.


**Command Retry Categories and Requirements**


For command retry purposes, an outstanding command is in one of three categories:

  - **Unrestricted Retry** : The outstanding command is an idempotent command (refer to section
9.6.3.1) that is able to be retried without restrictions because that outstanding command has no
effect on user data or NVM subsystem state (e.g., an NVM Command Set Read command). Refer
to section 9.6.3.2.1.

  - **Delayed Retry** : The outstanding command is an idempotent command for which any retry and/or
reporting of the result of that retry is required to be delayed until no further controller processing is
possible of that outstanding command because the outstanding command modifies user data or
NVM subsystem state (e.g., an NVM Command Set Write command, except as described in section
9.6.3.2.2). Refer to section 9.6.3.2.2.

  - **State**   - **Dependent Retry** : The outstanding command is not an idempotent command (e.g., a
Namespace Management command that creates a namespace) or is an idempotent command that
is able to affect behavior of other hosts. The procedures for recovery from such an outstanding
command depend on the extent, if any, to which that outstanding command has been processed
by the controller. Refer to section 9.6.3.2.3.


Sections 9.6.3.2.1, 9.6.3.2.2, and 9.6.3.2.3 define each command retry category and describe host
requirements and restrictions that prevent retry of outstanding commands from corrupting user data or
making unintended changes to NVM subsystem state.


**9.6.3.2.1** **Unrestricted Retry Commands**


An outstanding command is an Unrestricted Retry command if that command:


a) is an idempotent command (refer to section 9.6.3.1); and
b) does not change more than ancillary state in the NVM subsystem (e.g., statistics such as the value

of the Data Units Read field in the SMART / Health Information log page (refer to Figure 207)).


For an Unrestricted Retry command:

  - the Controller Capability Change (CCC) bit;

  - the Namespace Inventory Change (NIC) bit;


666


NVM Express [®] Base Specification, Revision 2.2


  - the Namespace Capability Change (NCC) bit; and

  - the Logical Block Content Change (LBCC) bit


are all cleared to ‘0’ in the Commands Supported and Effects data structure (refer to Figure 211) in the
Commands Supported and Effects log page (refer to section 5.1.12.1.6). If any of these four bits is set to
‘1’, then that command is not an Unrestricted Retry command.


A host may retry any outstanding command that is an Unrestricted Retry command immediately after
communication loss without determining whether further controller processing of that outstanding command
is possible.


For recovery purposes, a host may treat any outstanding command that is an Unrestricted Retry command
as if that command were a Delayed Retry command or a State-Dependent Retry command.


**9.6.3.2.2** **Delayed Retry Commands**


An outstanding command is a Delayed Retry command if that command:


a) is an idempotent command (refer to section 9.6.3.1); and
b) changes user data or NVM subsystem state (e.g., Read Recovery Level (refer to section 8.1.20) or

Reservation state (refer to section 8.1.22)),


unless the changes to user data or NVM subsystem state are able to affect the behavior of any other host
(e.g., refer to the example in Annex B.6.4). As explained further in Annex B.6.4, use of individual Delayed
Retry commands (e.g., an NVM Command Set Write command) that are not part of a fused operation to
affect the behavior of other hosts is strongly discouraged.


A host should treat an outstanding command that is a Delayed Retry command as having command
ordering requirements with respect to other commands where those command ordering requirements are
enforced by higher-level software (refer to section 3.4.1). Hence, for any such command, a host should not
report completion or error status, including errors caused by communication loss, to higher-level software
(e.g., an associated application, filesystem or database) until the host has determined that no further
controller processing of that command and retries, if any, of that command is possible. If a host violates
this recommendation, corruption of user data and unintended changes to NVM subsystem state are
possible; refer to Annex B.6.1 for an example where user data is corrupted.


A host is able to comply with this “should not report” recommendation by delaying submission of a retry of
any outstanding command that is a Delayed Retry command until no further controller processing is
possible of the original outstanding command and any previously submitted retries of that command. This
avoids host delays in reporting completion of any command upon receiving the CQE for that command.


A host may treat any outstanding command that is a Delayed Retry command as if that command were a
State-Dependent Retry command.


A host that does not adhere to the recommendations in this section for handling outstanding commands
that are Delayed Retry commands risks causing corruption of user data. It is strongly recommended that
host NVMe implementations adhere to these recommendations to avoid data corruption.


**9.6.3.2.3** **State-Dependent Retry Commands**


An outstanding command is a State-Dependent Retry command if the command changes user data or NVM
subsystem state, and the command:


a) is not an idempotent command (refer to section 9.6.3.1); or
b) changes user data or NVM subsystem state in a way that is able to affect the behavior of other

hosts.


A host should not retry an outstanding command that is a State-Dependent Retry command without first
determining that command retry is the appropriate recovery action. This is because retrying such a
command may have different results than the original command, duplicate the results of the original
command, or affect the behavior of other hosts in a different manner than the original command. In general,
determination of the appropriate recovery action is only able to be performed by higher-level software (e.g.,


667


NVM Express [®] Base Specification, Revision 2.2


an associated application, filesystem or database) that is able to determine the extent, if any, to which the
outstanding command has been processed and enforce ordering requirements among commands (refer to
section 3.4.1).


A host should treat an outstanding command that is a State-Dependent Retry command as having
command ordering requirements enforced by higher-level software with respect to other commands (refer
to section 3.4.1). Hence, for any such command, a host should not report completion or error status,
including errors caused by communication loss, to higher-level software (e.g., an associated application, a
filesystem or database), until the host has determined that no further controller processing of the
outstanding command and retries, if any, of that command is possible. If a host violates this
recommendation, corruption of user data or unintended changes to NVM subsystem state are possible;
refer to Annex B.6.2 for an example where unintended changes occur to NVM subsystem state.


A host that does not adhere to the recommendations in this section for handling outstanding commands
that are State-Dependent Retry commands risks causing corruption of user data and unintended changes
to NVM subsystem state. It is strongly recommended that host NVMe implementations adhere to these
recommendations to avoid these outcomes.


668


