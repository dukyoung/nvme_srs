NVM Express NVM Command Set Specification, Revision 1.2


116


**5 Extended Capabilities**

**5.1**

**Asymmetric Namespace Access Reporting**

Asymmetric Namespace Access Reporting operates as defined in the NVM Express Base Specification
with additional definitions specific to the NVM Command Set.
Figure 133 describes Asymmetric Namespace Access effects on command processing that are specific to
the NVM Command Set and its associated Feature Identifiers.

**Figure 133: ANA effects on NVM Command Set Command Processing**

**Command**

**ANA State**

**Effects on command processing**

Get Features
ANA Inaccessible,
ANA Persistent Loss, or
ANA Change
The following NVM Command Set specific feature identifiers are not
available1:

a)
Error Recovery (i.e., 05h).
Identify
ANA Inaccessible or
ANA Persistent Loss
Capacity fields in the Identify Namespace data structure (refer to
Figure 114) information are cleared to 0h.

Set Features
ANA Inaccessible
The saving of features shall not be supported and the following
NVM Command Set specific feature identifiers are not available1:

a)
Error Recovery (i.e., 05h).

ANA Change
The saving of features shall not be supported and the following
NVM Command Set specific feature identifiers are not available1:

a)
Error Recovery (i.e., 05h).
Notes:
1.
If the ANA state is ANA Inaccessible State, then commands that use feature identifiers or log pages that are not
available shall abort with a status code of Asymmetric Access Inaccessible. If the ANA state is ANA Persistent
Loss State, then commands that use feature identifiers or log pages that are not available shall abort with a
status code of Asymmetric Access Persistent Loss. If the ANA state is ANA Change State, then commands that
use feature identifiers or log pages that are not available shall abort with a status code of Asymmetric Access
Transition.

**5.2**

**Command Set Specific Capability**

**Get LBA Status**
The Get LBA Status capability enables the host to obtain information about LBAs:
•
Identifying LBAs that may be allocated in a namespace provides the host with the ability to minimize
the user data accessed when copying that namespace for use cases such as namespace migration
and snapshots. The Get LBA Status capability provides the host the ability to identify logical blocks
that may be allocated in a namespace.
•
Potentially Unrecoverable LBAs are LBAs that, when read, may result in the command that caused
the media to be read being aborted with a status code of Unrecovered Read Error. The Get LBA
Status capability provides the host with the ability to identify Potentially Unrecoverable LBAs. The
logical block data and metadata, if any, are able to be recovered from another location and re-
written.
If the Get LBA Status capability is supported, then the controller shall support the Get LBA Status command.


||Command|||ANA State|||Effects on command processing||
|---|---|---|---|---|---|---|---|---|
|Get Features|||ANA Inaccessible,<br>ANA Persistent Loss, or<br>ANA Change|||The following NVM Command Set specific feature identifiers are not<br>1<br>available :<br>a) Error Recovery (i.e., 05h).|||
|Identify|||ANA Inaccessible or<br>ANA Persistent Loss|||Capacity fields in the Identify Namespace data structure (refer to<br>Figure 114) information are cleared to 0h.|||
|Set Features|||ANA Inaccessible|||The saving of features shall not be supported and the following<br>1<br>NVM Command Set specific feature identifiers are not available :<br>a) Error Recovery (i.e., 05h).|||
||||ANA Change|||The saving of features shall not be supported and the following<br>1<br>NVM Command Set specific feature identifiers are not available :<br>a) Error Recovery (i.e., 05h).|||
|Notes:<br>1. If the ANA state is ANA Inaccessible State, then commands that use feature identifiers or log pages that are not<br>available shall abort with a status code of Asymmetric Access Inaccessible. If the ANA state is ANA Persistent<br>Loss State, then commands that use feature identifiers or log pages that are not available shall abort with a<br>status code of Asymmetric Access Persistent Loss. If the ANA state is ANA Change State, then commands that<br>use feature identifiers or log pages that are not available shall abort with a status code of Asymmetric Access<br>Transition.|||||||||

117
If Action Types 10h and 11h are supported (refer to the Get LBA Status Supported (GLSS) bit in the Optional
Admin Command Support (OACS) field in the Identify Controller data structure), then the controller shall:
•
support LBA Status Information Alert Notices (refer to the Optional Asynchronous Events
Supported (OAES) field in the Identify Controller data structure);
•
support the LBA Status Information log page;
•
support the Log Page Offset and extended Number of Dwords (i.e., 32 bits rather than 12 bits) in
the Get Log Page command (refer to the Attributes field of the Identify Controller data structure);
and
•
support the LBA Status Information Attributes Feature.
Prior to using a Get LBA Status command with the Action Type (ATYPE) field values 10h or 11h:
•
The host should use the Get Features and Set Features commands with the LBA Status Information
Attributes Feature (refer to section 4.1.3.5) to retrieve and optionally configure the LBA Status
Information Report Interval; and
•
If the host wishes to receive LBA Status Information Alert asynchronous events, the host should
enable LBA Status Information Alert Notices (refer to Figure 98).
If LBA Status Information Alert Notices are enabled, the controller shall send an LBA Status Information
Alert asynchronous event if:
a) there are Tracked LBAs and:
a) the LBA Status Information Report Interval condition has been exceeded; or
b) an implementation specific aggregate threshold, if any exists, of Tracked LBAs has been
exceeded;
or
b) a component (e.g., die or channel) failure has occurred that may result in the controller aborting
commands with a status code of Unrecovered Read Error.
Upon receiving an LBA Status Information Alert asynchronous event, the host should send one or more
Get Log Page commands for Log Page Identifier 0Eh with the Retain Asynchronous Event bit set to ‘1’ to
read the LBA Status Information log page (refer to section 4.1.4.5).
Once the host has started reading the LBA Status Information log page with the Retain Asynchronous Event
bit set to ‘1’, the controller shall not modify the contents of that log page until the host reads the LBA Status
Information log page with the Retain Asynchronous Event bit cleared to ‘0’.
The LBA Status Information log page returns zero or more sets of per-namespace LBA Range Descriptors.
Each LBA Range Descriptor specifies a range of LBAs that should be examined by the host in a subsequent
Get LBA Status command (refer to section 4.2.1).
The Get LBA Status command requests information about Potentially Unrecoverable LBAs in a specified
range.
The LBA Status Information Report Interval is restarted by the controller when the host issues a Get Log
Page command for Log Page Identifier 0Eh with the Retain Asynchronous Event bit cleared to ‘0’. Issuing
a Get Log Page command for Log Page Identifier 0Eh with the Retain Asynchronous Event bit cleared to
‘0’ causes an outstanding LBA Status Information Alert asynchronous event to be cleared if there is one
outstanding on the controller.
118
When the host re-reads the header of the LBA Status Information log page with the Retain Asynchronous
Event bit cleared to ‘0’, the host should ensure that the LBA Status Generation Counter matches the original
value read. If these values do not match, there is newer LBA Status Information log page data available
than the data returned the previous time the host read the LBA Status Information log page. In this case,
the host is not required to wait for the LBA Status Information Poll Interval (LSIPI) to pass before re-reading
the LBA Status Information log page.
The host decides when to send Get LBA Status commands and when to recover the LBAs identified by the
Get LBA Status commands, relative to when the host issues a Get Log Page command for Log Page
Identifier 0Eh with the Retain Asynchronous Event bit cleared to ‘0’. Section 5.2.1.1 describes some
example host implementations.
The Get LBA Status command may return zero or more LBA Status Descriptors (refer to Figure 131) for
each LBA Range Descriptor (refer to Figure 111) returned by the LBA Status Information log page.

**Figure 134: Example LBA Status Log Namespace Element returned by LBA Status Information**

**Log Page**

**Bytes**

**Description**

**Value**
03:00

**Namespace Element Identifier (NEID)**
07:04

**Number of LBA Range Descriptors**

**(NLRD)**

**Recommended Action Type (RATYPE)**
11h (i.e., Tracked LBAs)
15:09
Reserved
0h

31:16

**LBA Range Descriptor 0: This field**
contains the first LBA Range Descriptor in
this LBA Status Log Namespace Element.

**Bytes**

**Description**

**Value**
07:00

**Range Starting LBA (RSLBA)**
11:08

**Range Number of Logical Blocks**

**(RNLB)**
1,000
15:12
Reserved
0h

47:32

**LBA Range Descriptor 1: This field**
contains
the
second
LBA
Range
Descriptor in this LBA Status Log

**Namespace Element.**

**Bytes**

**Description**

**Value**
07:00

**Range Starting LBA (RSLBA)**
15,000
11:08

**Range Number of Logical Blocks**

**(RNLB)**
15,010
15:12
Reserved
0h

**Figure 135: Example LBA Status Descriptors for Get LBA Status Command issued for LBA**

**Range Descriptor 0 in Figure 134 (RSLBA set to 10, RNLB set to 1,000)**

**Bytes**

**Description**

**Value**
03:00

**Number of LBA Status Descriptors (NLSD)**

**Completion Condition (CMPC)**
07:05
Reserved
0h

23:08

**LBA Status Descriptor Entry 0: This field**
contains the first LBA Status Descriptor Entry
in this list.

**Bytes**

**Description**

**Value**
07:00

**Descriptor Starting LBA (DSLBA)**
11:08

**Number of Logical Blocks (NLB)**
…
…
…


||Bytes|||Description|||Value|||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|03:00|||Namespace Element Identifier (NEID)|||1||||||||||
|07:04|||Number of LBA Range Descriptors<br>(NLRD)|||2||||||||||
|08|||Recommended Action Type (RATYPE)|||11h (i.e., Tracked LBAs)||||||||||
|15:09|||Reserved|||0h||||||||||
|31:16|||LBA Range Descriptor 0: This field<br>contains the first LBA Range Descriptor in<br>this LBA Status Log Namespace Element.||||Bytes|||Description|||Value|||
||||||||07:00||Range Starting LBA (RSLBA)|||10||||
||||||||11:08||Range Number of Logical Blocks<br>(RNLB)|||1,000||||
||||||||15:12||Reserved|||0h||||
|47:32|||LBA Range Descriptor 1: This field<br>contains the second LBA Range<br>Descriptor in this LBA Status Log<br>Namespace Element.||||Bytes|||Description|||Value|||
||||||||07:00||Range Starting LBA (RSLBA)|||15,000||||
||||||||11:08||Range Number of Logical Blocks<br>(RNLB)|||15,010||||
||||||||15:12||Reserved|||0h||||


||Bytes|||Description||Value||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|03:00|||Number of LBA Status Descriptors (NLSD)||3|||||||||||
|04|||Completion Condition (CMPC)||2|||||||||||
|07:05|||Reserved||0h|||||||||||
|23:08|||LBA Status Descriptor Entry 0: This field<br>contains the first LBA Status Descriptor Entry<br>in this list.||||Bytes|||Description|||Value|||
|||||||07:00|||Descriptor Starting LBA (DSLBA)|||10||||
|||||||11:08|||Number of Logical Blocks (NLB)|||30||||
|||||||…|||…|||…||||

119

**Figure 135: Example LBA Status Descriptors for Get LBA Status Command issued for LBA**

**Range Descriptor 0 in Figure 134 (RSLBA set to 10, RNLB set to 1,000)**

**Bytes**

**Description**

**Value**

39:24

**LBA Status Descriptor Entry 1: This field**
contains the second LBA Status Descriptor

**Entry in this list.**

**Bytes**

**Description**

**Value**

**07:00**

**Descriptor**

**Starting**

**LBA**

**(DSLBA)**

**11:08**

**Number**

**of**

**Logical**

**Blocks**

**(NLB)**

**…**

**…**
…

55:40

**LBA Range Descriptor 2: This field contains**
the third LBA Status Descriptor Entry in this

**list.**

**Bytes**

**Description**

**Value**

**07:00**

**Descriptor**

**Starting**

**LBA**

**(DSLBA)**
1,000

**11:08**

**Number of Logical Blocks**

**(NLB)**

**…**

**…**
…

**Figure 136: Example LBA Status Descriptors for Get LBA Status Command issued for LBA**

**Range Descriptor 1 in Figure 134 (RSLBA set to 15,000, RNLB set to 15,010)**

**Bytes**

**Description**

**Value**
03:00

**Number of LBA Status Descriptors (NLSD)**

**Completion Condition (CMPC)**
07:05
Reserved
0h

23:08

**LBA Status Descriptor Entry 0: This field**
contains the only LBA Status Descriptor Entry
in this list.

**Bytes**

**Description**

**Value**

**07:00**

**Descriptor**

**Starting**

**LBA**

**(DSLBA)**
15,000

**11:08**

**Number**

**of**

**Logical**

**Blocks**

**(NLB)**
15,010

**…**

**…**
…

**5.2.1.1**

**Sample Get LBA Status Host Implementations (Informative)**

**5.2.1.1.1**

**Example Flow #1**
1) Read the LBA Status Information log page with RAE bit set to ‘1’;
2) Complete all necessary Get LBA Status commands;
3) Complete all necessary recovery of the affected user data by rewriting that data; and
4) Read the LBA Status Information log page header with RAE bit cleared to ‘0’.

**5.2.1.1.2**

**Example Flow #2**
1) Read the LBA Status Information log page with RAE bit set to ‘1’;
2) Read the LBA Status Information log page with RAE bit cleared to ‘0’;
3) Issue some host-determined subset of the Get LBA Status commands indicated by the log page
data;
4) Complete the recovery of the affected user data returned by the Get LBA Status commands issued
so far;
5) Re-issue the Get LBA Status commands over the ranges associated with the re-written (i.e.,
recovered) user data;


||Bytes|||Description|||Value|||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|39:24|||LBA Status Descriptor Entry 1: This field<br>contains the second LBA Status Descriptor<br>Entry in this list.|||||Bytes|Description||Value|||
||||||||07:00||Descriptor Starting LBA<br>(DSLBA)||550|||
||||||||11:08||Number of Logical Blocks<br>(NLB)||75|||
||||||||…||…||…|||
|55:40|||LBA Range Descriptor 2: This field contains<br>the third LBA Status Descriptor Entry in this<br>list.|||||Bytes||Description|Value|||
||||||||07:00||Descriptor Starting LBA<br>(DSLBA)||1,000|||
||||||||11:08||Number of Logical Blocks<br>(NLB)||10|||
||||||||…||…||…|||


||Bytes|||Description|||Value|||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|03:00|||Number of LBA Status Descriptors (NLSD)|||1||||||||
|04|||Completion Condition (CMPC)|||2||||||||
|07:05|||Reserved|||0h||||||||
|23:08|||LBA Status Descriptor Entry 0: This field<br>contains the only LBA Status Descriptor Entry<br>in this list.|||||Bytes||Description|Value|||
||||||||07:00|||Descriptor Starting LBA<br>(DSLBA)|15,000|||
||||||||11:08|||Number of Logical Blocks<br>(NLB)|15,010|||
||||||||…|||…|…|||

120
6) Confirm that the re-written LBAs are no longer in the Tracked LBA List (if any are still there, they
are there because they have been detected as newly bad again);
7) Add any new LBA ranges returned in the Get LBA Status commands to the list of LBAs still
outstanding the host needs to recover; and
8) If the host has not processed all LBA ranges returned by:
•
the LBA Status Information log page in step 1; and
•
the Get LBA Status command(s) in step 7,
then go back to step 3.

**Improving Performance through I/O Size and Alignment Adherence**
I/O controllers may require constrained I/O sizes and alignments to achieve the full performance potential.
There are several optional attributes that the controller uses to indicate these recommendations. If hosts
do not follow these constraints, then the controller shall function correctly, but performance may be limited.
For best write performance, the host should issue Write command, Write Uncorrectable command, Write
Zeroes command, and the write portion of the Copy command that specify:
a) a number of logical blocks that is:
a. a multiple of the Namespace Preferred Write Granularity (NPWG) field (refer to Figure
114), if the NPWG field is defined; and
b. a multiple of the number of logical blocks indicated by the Stream Write Size (SWS) field
(refer to the Streams Directive – Return Parameters Data Structure figure in the NVM
Express Base Specification), if the Streams Directive is enabled;
and
b) a Starting LBA (SLBA) field that is aligned to the Namespace Preferred Write Alignment (NPWA)
field (refer to Figure 114), if the NPWA field is defined.
Resolving conflicts between namespace attributes and Streams attributes is described in section 5.2.2.1.
The namespace preferred deallocate granularity is a number of logical blocks that is indicated by both the
NPDG field (refer to Figure 114) and the NPDGL field. The NPDGL field is able to represent larger values
than the NPDG field (refer to Figure 118). Support for these fields is indicated by the OPTPERF field (refer
to Figure 114). If the NPDG field and the NPDGL field are both supported and indicate different values of
namespace preferred deallocate granularity, then the host should use the value indicated by the NPDGL
field.
The namespace preferred deallocate alignment is a number of logical blocks that is indicated by both the
NPDA field (refer to Figure 114) and the NPDAL field (refer to Figure 118). The NPDAL field is able to
represent larger values than the NPDA field. Support for these fields is indicated by the OPTPERF field
(refer to Figure 114). If the NPDA field and the NPDAL field are both supported and indicate different non-
zero values of namespace preferred deallocate alignment, then the host should use the value indicated by
the NPDAL field. The NPDA field is a 0-based number (i.e., at least one is required to be defined) and the
NPDAL field is a 1-based number (i.e., a value of 0h indicates not supported).
For best performance, the host should issue Dataset Management commands with the Attribute –
Deallocate (AD) bit set to ‘1’ that specify:
a) a Length in Logical Blocks field that is a multiple of the namespace preferred deallocate granularity,
if the namespace preferred deallocate granularity is defined; and
121
b) a Starting LBA field that is:
a. a multiple of the namespace preferred deallocate alignment, if the namespace preferred
deallocate alignment is defined; and
b. a multiple of the Stream Granularity Size (SGS) field (refer to the Streams Directive –
Return Parameters Data Structure figure in the NVM Express Base Specification) if the
Streams Directive is enabled.
For best read performance, the host should issue Compare command, Read command, Verify command
and the read portion of the Copy command that specify:
a) a number of logical blocks that is a multiple of the Namespace Preferred Read Granularity (NPRG)
field (refer to Figure 118), if the NPRG field is supported; and
b) a Starting LBA (SLBA) field that is aligned to the Namespace Preferred Read Alignment (NPRA)
field (refer to Figure 118), if the NPRA field is supported.

**5.2.2.1**

**Improved I/O examples (Informative)**
It is recommended that the host utilize the I/O attributes as reported by the I/O controller to receive optimal
performance from the NVM subsystem. This section summarizes performance related attributes from
namespaces, streams, NVM Sets and the NVM command set. The I/O commands discussed throughout
this section include those that interact with non-volatile medium in either a Read, Compare, Copy, Verify,
Write, Write Uncorrectable, Write Zeroes operation, or Dataset Management operation with the Attribute -
Deallocate bit set to ‘1’. The I/O command properties of length and alignment are discussed throughout this
section.

**Figure 137: An example namespace with four NOIOBs**

In Figure 137 an example namespace is diagrammed with three Namespace I/O Boundaries (NOIOB) (refer
to Figure 114). The NOIOB attribute should be applied to read and write commands as specified in section
5.2.2. An I/O command may see its performance limited if that I/O command does not conform to the NOIOB
attribute considerations described in this section. The four green lines are example I/O commands from the
host that adhere to the recommendations of NOIOB settings for this namespace. None of the four I/O
commands shown in green on the top of Figure 137 cross an NOIOB. The three I/O commands shown in
red on the bottom of Figure 137 violate the recommendations for improved performance. The longest I/O
command shown in red crosses one NOIOB and ends aligned with a different NOIOB. The remaining two
I/O commands shown in red also cross an NOIOB. All three of these example I/O commands shown in red
are able to be split into two I/O commands that adhere to the recommendations provided by the namespace
for NOIOB.
122

**Figure 138: Example namespace illustrating a potential NABO and NABSN**

Continuing with the same namespace example from Figure 137, an illustration of Namespace Atomic
Boundary Offset (NABO) (refer to Figure 114) and Namespace Atomic Boundary Size Normal (NABSN)
(refer to Figure 114) is shown in Figure 138. NABSN and NABO attributes apply to Write, Write
Uncorrectable, and Write Zeroes commands. NABSN and NOIOB may not be related to each other, and
there may be an offset of NABO to locate the first NABSN starting. The NOIOBs are not shown in Figure
138. The I/O commands shown in green on the top of Figure 138 illustrate I/O commands that adhere to
the namespace’s guidance for optimal performance. The I/O commands shown in red on the bottom
illustrate I/O commands that do not follow the optimal performance guidelines.
The I/O command examples shown in red in Figure 137 and Figure 138 both illustrate commands that are
able to be restructured to conform to the namespace attributes for Optimal I/O relative to NOIOB, NABO,
and NABSN. Each of these example I/O commands shown in red in Figure 137 and Figure 138 are able to
be split into two different I/O commands that adhere to the recommendations. While this increases the
number of commands sent to the controller, the expectation is that adherence to the boundary
recommendations improves the performance for the controller. Avoiding host traffic that demands non-
optimal I/O commands is the most recommendable solution for a host.

**5.2.2.2**

**Alignment and Write Performance**
NPWG and NPWA are namespace internal constructs, and they are illustrated in Figure 139. The box at
the top of Figure 139 is the namespace. The series of boxes in the middle layer indicate many namespace
optimal write units described by NPWA (refer to Figure 114) and NPWG (refer to Figure 114), and the
bottom layer is a series of eight logical blocks that in aggregate form the NPWG for this example.
Sometimes NPWG are useful because several sequential logical blocks (refer to Figure 114) may be placed
and tracked together on the media, or the NPWG may be related to NVM subsystem data reliability
implementation constraints.
123

**Figure 139: Example namespace broken down to illustrate potential NPWA and NPWG settings**

Namespace

NPWG
logical block
NPWA

NPWG

**Legend**

Namespace Preferred Write Alignment (NPWA)
Conformant I/O
Non-Conformant I/O

Namespace Preferred Write Granularity (NPWG)

For a list of commands that apply to NPWG and NPWA attributes refer to section 5.2.2.

**5.2.2.3**

**Alignment and Read Performance**
NPRG and NPRA are namespace internal constructs, and they are illustrated in Figure 140. The box at the
top of Figure 140 is the namespace. The series of boxes in the middle layer indicate many namespace
optimal read units described by NPRA (refer to Figure 118) and NPRG (refer to Figure 118). In the figure,
the read alignment is 4 logical blocks. The bottom layer is a series of eight logical blocks that in aggregate
form the NPRG for this example. Sometimes NPRG are useful because several sequential logical blocks
(refer to Figure 118) may be placed and tracked together on the media, or the NPRG may be related to
NVM subsystem data reliability implementation constraints. Host reads that are of a length less than NPRA
may see their performance impacted if they violate read alignment as described in Figure 118.
124

**Figure 140: Example namespace broken down to illustrate potential NPRA and NPRG settings**

Namespace

NPRG
logical block
NPRA

NPRG

**Legend**

Namespace Preferred Read Alignment (NPRA)
Conformant I/O
Non-Conformant I/O

Namespace Preferred Read Granularity (NPRG)

The host should issue reads that meet the recommendations of NPRG and NPRA and may achieve optimal
read performance by issuing reads that meet the recommendation of NORS. If NORS is greater than NPRG,
reads that are a multiple of NPRG and not equal to NORS may see improved performance; however, read
performance may not be optimal.
Non-adherence to write-related performance attributes (i.e., NPWG, NPWA, NPDG, NPDGL, NPDA,
NPDAL, and NOWS), across all the namespaces in:
a) the same NVM Set;
b) the same Endurance Group when NVM Sets are not supported; or
c) the NVM subsystem when Endurance Groups are not supported,
may affect the level of read optimization achievable through the usage of NORS as described in this section.
For a list of commands that apply to NPRG and NPRA attributes refer to section 5.2.2.
125

**Figure 141: Non-conformant Write Impact**

Shown in Figure 141 is an I/O command that covers three of eight logical blocks within an NPWG. In this
example namespace, NPWG is set to eight logical blocks, and the write of only three logical blocks requires
a read of the preceding two logical blocks and trailing three logical blocks. The host write that completes to
the non-volatile medium consists of five logical blocks of older data and three new logical blocks with the
data provided by the write I/O command. The resulting read-modify-write may have non-optimal
performance in comparison to a host write adhering to the NPWG attribute due to the extra read operation
executed internally in the NVM subsystem. Aligning the beginning of the write I/O command with the NPWA
attribute removes the requirement to read the preceding existing data. Host writes with a length that is a
multiple of NPWG removes the requirement for reading the trailing data.
Following the NPWG recommendation alone is insufficient for optimal performance. If a write I/O command
specifies the number of LBAs that is an integer multiple of NPWG and is offset in alignment from the
recommended NPWA, then a read-modify-write may occur on the logical blocks at the beginning and ending
of the command. The I/O commands shown in red in Figure 139 specify numbers of LBAs that are integer
multiples of NPWG, but their alignment is triggering a read-modify-write at both the beginning and ending
of the write I/O command. The write I/O commands shown in green adhere to the alignment and granularity
requirements of the NPWA and NPWG. Figure 142 illustrates the shorter dark green write I/O command
that adheres to both NPWG and NPWA attributes. This dark green write I/O command has a length equaling
the NPWG attribute which adheres to the NPWG attribute recommendations. Figure 143 illustrates the dark
red write I/O command that follows the NPWG attribute with a length of one NPWG, but that command
does not adhere to the NPWA attribute recommendations. The dark red write I/O command requires a read
of the old data at the beginning and the ending of the write I/O command to fill both NPWG units illustrated
here. Longer write I/O commands that fail to adhere to the NPWA recommendation may trigger a read-
modify-write of the leading and trailing NPWG segments inside of the NVM subsystem.

**Figure 142: Host write I/O command following NPWA and NPWG**
126

**Figure 143: Host write I/O command following NPWG but not NPWA attributes**

The namespace preferred deallocate granularity and the namespace preferred deallocate alignment (refer
to section 5.2.2) are attributes of the namespace that are intended to improve performance for Dataset
Management deallocate operations within a namespace. The namespace preferred deallocate granularity
and the namespace preferred deallocate alignment may be impacted by multiple factors including but not
limited to the boundaries described in Figure 139, device hardware limits, or non-volatile medium erase
block sizes. Deallocating at multiples of the namespace preferred deallocate granularity and aligned to the
namespace preferred deallocate alignment (i.e., (Starting LBA modulo namespace preferred deallocate
alignment) == 0) may enable improved deallocate performance for the namespace.

**Figure 144: Two streams composed of SGS and SWS**

Streams (refer to the Streams Directive section in the NVM Express Base Specification) may or may not
be utilized with different namespace attributes.
The stream granularity length is a number of logical blocks that is the product of the Stream Granularity
Size (SGS) field and the number of logical blocks indicated by the Stream Write Size (SWS) field (refer to
the Streams Directive – Return Parameters Data Structure figure in the NVM Express Base Specification).
Figure 144 shows an example of the relationship between these attributes in which the SGS field is set to
4h. The first stream is composed of three SGS units, and each SGS unit in this example is equal to four
SWS units. A stream is optimized for performance of the Dataset Management command deallocate
operation if write I/O lengths are integer multiples of the stream granularity length. A stream is optimized
for write performance if write I/O lengths are integer multiples of the SWS field.
Streams are sometimes handled by separate I/O paths in the device. This may include different device
hardware, media mapping, or reliability protections. The number of logical blocks indicated by the SWS
field should be a multiple of the number of logical blocks indicated by the NPWG field. The size indicated
by the SGS field and the namespace preferred deallocate granularity may be equal to each other or
multiples of each other. If a namespace indicates integer multiple size relationships between the streams
attributes (the SWS field and the SGS field) and the namespace attributes (the NPWG field and the
127
namespace preferred deallocate granularity), then a write operation or a deallocate operation may obtain
optimal performance by specifying a number of logical blocks that is equal to the largest of those attributes.
Not all namespaces indicate their Streams attributes and namespace attributes in multiples as described
above. The recommended order of priority for a host to resolve conflicts between namespace attributes and
Streams attributes is to issue write operations that conform to the SGS field and the SWS field if the Streams
Directive is used. If the Streams Directive is not used, then issuing write operations that conform to the
namespace attributes should provide improved performance.
If the Streams Directive is enabled on a namespace, and a Dataspace Management command specifying
a deallocate operation specifies a range of logical blocks that are associated with a stream, then that range
should conform to the SGS based alignment and size preferences. If the Streams Directive is not enabled
on a namespace, or if the logical blocks specified by a range are not associated with a stream, then that
range should conform to the namespace preferred deallocate granularity and the namespace preferred
deallocate alignment.
Namespace Optimal Write Size (NOWS) (refer to Figure 114) is intended to supplement NVM Sets Optimal
Write Size as NOWS provides a mechanism to report the optimal write size that scales to a multiple
namespace per NVM Set use case, but also covers the use case where there is a single namespace that
exists in an NVM Set. Namespaces should report NOWS as a multiple of NPWG. When constructing write
operations, the host should minimally construct writes that meet the recommendations of NPWG and
NPWA, but may achieve optimal write performance by constructing writes that meet the recommendation
of NOWS.
If NVM Sets are supported as described in Figure 114, the value in the NOWS field for the namespace
indicates the value the host should use to achieve optimal performance. If an NVM Set does not specify an
Optimal Write Size, the host should use the value in the NOWS field for the namespace for I/O optimization
purposes. Similarly, if NOWS is not defined for a namespace, the host should use the value in the Optimal
Write Size field for the NVM Set associated with that namespace to achieve optimal performance.

**Metadata Handling**
The controller may support metadata per logical block. Metadata is additional data allocated on a per logical
block basis. There is no requirement for how the host makes use of the metadata area. One of the most
common usages for metadata is to convey end-to-end protection information.
The metadata may be transferred by the controller to or from the host in one of two ways. The mechanism
used is selected when the namespace is formatted.
The first mechanism for transferring the metadata is as a contiguous part of the logical block that the
metadata is associated with. The metadata is transferred at the end of the associated logical block, forming
an extended logical block. This mechanism is illustrated in Figure 145. In this case, both the logical block
data and logical block metadata are pointed to by the PRP1 and PRP2 pointers (or SGL Entry 1 if SGLs
are used).
128

**Figure 145: Metadata – Contiguous with LBA Data, Forming Extended LBA**

The second mechanism for transferring the metadata is as a separate buffer of data. This mechanism is
illustrated in Figure 146. In this case, the metadata is pointed to with the Metadata Pointer, while the logical
block data is pointed to by the Data Pointer. When a command uses PRPs for the metadata in the
command, the metadata is required to be physically contiguous. When a command uses SGLs for the
metadata in the command, the metadata is not required to be physically contiguous.

**Figure 146: Metadata – Transferred as Separate Buffer**

One of the transfer mechanisms shall be selected for each namespace when the namespace is formatted;
transferring a portion of metadata with one mechanism and a portion with the other mechanism is not
supported.
If end-to-end data protection is used, then the Protection Information field for each logical block is contained
in the metadata.

**5.3**

**End-to-end Data Protection**

To provide robust data protection from the application to the NVM media and back to the application itself,
end-to-end data protection may be used. If this optional mechanism is enabled, then additional protection
information (e.g., CRC) is added to the logical block that may be evaluated by the controller and/or the host
to determine the integrity of the logical block. This additional protection information, if present, is either the
first bytes of metadata or the last bytes of metadata, based on the format of the namespace (refer to the
PIP bit in the DPS field shown in Figure 114). If the value in the Metadata Size (refer to Figure 116) is
greater than the number of bytes of protection information and the protection information is contained in the
first bytes of the metadata, then the CRC does not cover any metadata bytes. If the Metadata Size is greater
than the number of bytes of protection information and the protection information is contained in the last
bytes of the metadata, then the CRC covers all metadata bytes up to but excluding the protection
information. As described in section 5.2.3, metadata and hence this protection information may be
configured to be contiguous with the logical block data or stored in a separate buffer.
The most commonly used data protection mechanisms in Enterprise implementations are SCSI Protection
Information, commonly known as Data Integrity Field (DIF), and the Data Integrity Extension (DIX). The
primary difference between these two mechanisms is the location of the protection information. In DIF, the
protection information is contiguous with the logical block data and creates an extended logical block, while
in DIX, the protection information is stored in a separate buffer. The end-to-end data protection mechanism
LBA  n Data
LBA  n +1  Data
Sector  N
Metadata
Sector  N+2
Metadata
Sector  N
Metadata
Sector  N+2
Metadata
Sector  N
Metadata
LBA  n +1
Metadata
LBA n
Metadata

**Host**
…

Data Buffer (PRP1 & PRP2)

Sector N Data
Sector N
Metadata
Sector N+1
Metadata
Sector N+2
Metadata

LBA n+1 Data
LBA n+2 Data
Sector N
Metadata
Sector N+1
Metadata
Sector N+2
Metadata
Sector N
Metadata
Sector N+1
Metadata
Sector N+2
Metadata
Sector N
Metadata
Sector N+1
Metadata
Sector N+2
Metadata
Sector N
Metadata
Sector N+1
Metadata
Sector N+2
Metadata
LBA n+1
Metadata
LBA n+2
Metadata


**Host**

…
…

Data Buffer (PRP1 & PRP2)
Metadata Buffer (MD)

LBA n Data
LBA n
Metadata


||Host|
|---|---|


|LBA n Data|SLeBctAo rn N<br>Metadata|LBA n+1 Data|SLeBctAo rn N+1+ 2<br>Metadata|
|---|---|---|---|


|SLeBctAo rn N<br>Metadata|SLeBctAo rn N+1+1<br>Metadata|SLeBctAo rn N+2+2<br>Metadata|
|---|---|---|


||Host|
|---|---|


|SLeBctAo rn N D Dataata|LBA n+1 Data|LBA n+2 Data|
|---|---|---|

129
defined by this specification is functionally compatible with both DIF and DIX. DIF functionality is achieved
by configuring the metadata to be contiguous with logical block data (as shown in Figure 145), while DIX
functionality is achieved by configuring the metadata and data to be in separate buffers (as shown in Figure
146).
The NVM Express interface supports the same end-to-end protection types defined in the SCSI Protection
information model specified in SBC-4. The type of end-to-end data protection (i.e., Type 1, Type 2, or Type
3) is selected when a namespace is formatted and is reported in the Identify Namespace data structure
(refer to Figure 114).

**Protection Information Formats**
The following protection information formats are defined:
a) 16b Guard Protection Information;
b) 32b Guard Protection Information; and
c) 64b Guard Protection Information.
The following protection information formats are defined as extended protection information formats and
are only supported when the Controller Attributes (CTRATT) field has the Extended LBA Formats
Supported (ELBAS) bit set to ‘1’ (refer to the Identify Controller data structure in the NVM Express Base
Specification):
a) 16b Guard Protection Information with the STS field set to a non-zero value;
b) 32b Guard Protection Information; and
c) 64b Guard Protection Information.

**5.3.1.1**

**16b Guard Protection Information**
If the Storage Tag Size (STS) field for the LBA Format is cleared to 0h, then the 16b Guard Protection
Information is shown in Figure 147 and is contained in the metadata associated with each logical block.
The Guard field contains a CRC-16 computed over the logical block data. The formula used to calculate
the CRC-16 is defined in SBC-4. In addition to a CRC-16, DIX also specifies an optional IP checksum that
is not supported by the NVM Express interface. The Application Tag is an opaque data field not interpreted
by the controller and that may be used to disable checking of protection information. The Reference Tag
associates logical block data with an address and protects against misdirected or out-of-order logical block
transfer. Like the Application Tag, the Reference Tag may also be used to disable checking of protection
information.
130

**Figure 147: 16b Guard Protection Information Format when STS field is cleared to 0h**
Bit

Byte
MSB
Guard
LSB
MSB
Application Tag
LSB
MSB

Reference Tag

LSB

If the Storage Tag Size (STS) field for the LBA Format is non-zero, then the 16b Guard Protection
Information is shown in Figure 148. The Storage and Reference Space field is separated into a Storage
Tag field and a Logical Block Reference Tag field as defined in section 5.3.1.4. The Storage Tag field is an
opaque data field not interpreted by the controller. The Logical Block Reference Tag field associates logical
block data with an address and protects against misdirected or out-of-order logical block transfer. The
Logical Block Reference Tag field may be used to disable checking of protection information.

**Figure 148: 16b Guard Protection Information Format when STS field is non-**

**zero**
Bit

Byte
MSB
Guard
LSB
MSB
Application Tag
LSB
MSB

Storage and Reference Space

LSB

**5.3.1.2**

**32b Guard Protection Information**
The 32b Guard Protection Information is shown in Figure 149 and is contained in the metadata associated
with each logical block. The 32b Guard Protection Information shall only be available to namespaces that
have a logical block size (refer to the LBADS field in Figure 116) greater than or equal to 4 KiB.
The Guard field contains a 32b CRC computed over the logical block data. The formula used to calculate
the CRC is the CRC-32C (Castagnoli) which uses the generator polynomial 1EDC6F41h (refer to the NVM
Express Management Interface Specification). The Application Tag and Storage and Reference Space
fields have the same definition as defined by 16b Guard Protection Information (refer to section 5.3.1.1).
131

**Figure 149: 32b Guard Protection Information Format**
Bit

Byte
MSB

Guard

LSB
MSB
Application Tag
LSB
MSB

Storage and Reference Space

LSB

**5.3.1.2.1**

**32b CRC Test Cases**
Several 32b CRC test cases are shown in Figure 150.

**Figure 150: 32b CRC Test Cases for 4 KiB Logical Block with no Metadata**

**Logical Block Contents**

**32b Guard Field Value**
4 KiB bytes each byte cleared to 00h
98F94189h
4 KiB bytes each byte set to FFh
25C1FE13h
4 KiB bytes of an incrementing byte pattern from 00h to FFh, repeating (e.g., byte 0 is
set to 00h, byte 1 is set to 01h, … , byte 254 is set to FEh, byte 255 is set to FFh, byte
256 is set to 00h, …)
9C71FE32h

4 KiB bytes of a decrementing pattern from FFh to 00h, repeating (e.g., byte 0 is set to
FFh, byte 1 is set to FEh, … , byte 254 is set to 01h, byte 255 is set to 00h, byte 256 is
set to FFh, …)
214941A8h

**5.3.1.3**

**64b Guard Protection Information**

The 64b Guard Protection Information is shown in Figure 151 and is contained in the metadata associated
with each logical block. 64b Guard Protection Information shall only be available to namespaces that have
a logical block size (refer to the LBADS field in Figure 116) greater than or equal to 4 KiB.
The Guard field contains a 64b CRC computed over the logical block data. The polynomial used to calculate
the CRC is defined in section 5.3.1.3.1. The Application Tag and Storage and Reference Space have the
same definition as defined by 16b Guard Protection Information (refer to section 5.3.1.1).


||Figure 150: 32b CRC Test Cases for 4 KiB Logical Block with no Metadata||||
|---|---|---|---|---|
||Logical Block Contents||32b Guard Field Value||
|4 KiB bytes each byte cleared to 00h|||98F94189h||
|4 KiB bytes each byte set to FFh|||25C1FE13h||
|4 KiB bytes of an incrementing byte pattern from 00h to FFh, repeating (e.g., byte 0 is<br>set to 00h, byte 1 is set to 01h, … , byte 254 is set to FEh, byte 255 is set to FFh, byte<br>256 is set to 00h, …)|||9C71FE32h||
|4 KiB bytes of a decrementing pattern from FFh to 00h, repeating (e.g., byte 0 is set to<br>FFh, byte 1 is set to FEh, … , byte 254 is set to 01h, byte 255 is set to 00h, byte 256 is<br>set to FFh, …)|||214941A8h||

132

**Figure 151: 64b Guard Protection Information Format**
Bit

Byte
MSB

Guard

LSB
MSB
Application Tag
LSB
MSB

Storage and Reference Space

LSB

**5.3.1.3.1**

**64b CRC Definition**
Figure 152 defines the 64b CRC polynomial used to generate the Guard field for the 64b Guard Protection
Information.

**Figure 152: 64b CRC Polynomials**

**Function**

**Definition**

F(x)
A polynomial representing the transmitted logical block data, which is covered by the 64b CRC. For the
purposes of the 64b CRC, the coefficient of the highest order term shall be byte zero bit seven of the
logical block data and the coefficient of the lowest order term shall be bit zero of the last byte of the
logical block data.
F’(x)
A polynomial representing the received logical block data.

G(x)
The generator polynomial:
G(x) = x64 + x63 + x61 + x59 + x58 + x56 + x55 + x52 + x49 + x48 + x47 + x46 + x44 + x41 + x37 + x36 +
x34 + x32 + x31 + x28 + x26 + x23 + x22 + x19 + x16 + x13 + x12 + x10 + x9 + x6 + x4 + x3 + x0
(i.e., in finite field notation G(x) = 1_ AD93D235_94C93659h)
R(x)
The remainder polynomial calculated during CRC generation by the transmitter, representing the
transmitted Guard field.
R’(x)
A polynomial representing the received Guard field.
RB(x)
The remainder polynomial calculated during CRC checking by the receiver.
RB(x) = 0 indicates no error was detected.
RC(x)
The remainder polynomial calculated during CRC checking by the receiver.
RC(x) = 0 indicates no error was detected.
QA(x)
The quotient polynomial calculated during CRC generation by the transmitter.
The value of QA(x) is not used.


||Function|||Definition||
|---|---|---|---|---|---|
|F(x)|||A polynomial representing the transmitted logical block data, which is covered by the 64b CRC. For the<br>purposes of the 64b CRC, the coefficient of the highest order term shall be byte zero bit seven of the<br>logical block data and the coefficient of the lowest order term shall be bit zero of the last byte of the<br>logical block data.|||
|F’(x)|||A polynomial representing the received logical block data.|||
|G(x)|||The generator polynomial:<br>G(x) = x64 + x63 + x61 + x59 + x58 + x56 + x55 + x52 + x49 + x48 + x47 + x46 + x44 + x41 + x37 + x36 +<br>x34 + x32 + x31 + x28 + x26 + x23 + x22 + x19 + x16 + x13 + x12 + x10 + x9 + x6 + x4 + x3 + x0<br>(i.e., in finite field notation G(x) = 1 AD93D235 94C93659h)|||
|R(x)|||_ _<br>The remainder polynomial calculated during CRC generation by the transmitter, representing the<br>transmitted Guard field.|||
|R’(x)|||A polynomial representing the received Guard field.|||
|RB(x)|||The remainder polynomial calculated during CRC checking by the receiver.<br>RB(x) = 0 indicates no error was detected.|||
|RC(x)|||The remainder polynomial calculated during CRC checking by the receiver.<br>RC(x) = 0 indicates no error was detected.|||
|QA(x)|||The quotient polynomial calculated during CRC generation by the transmitter.<br>The value of QA(x) is not used.|||

133

**Figure 152: 64b CRC Polynomials**

**Function**

**Definition**
QB(x)
The quotient polynomial calculated during CRC checking by the receiver.
The value of QB(x) is not used.
QC(x)
The quotient polynomial calculated during CRC checking by the receiver.
The value of QC(x) is not used.
M(x)
A polynomial representing the transmitted logical block data followed by the transmitted Guard field.
M’(x)
A polynomial representing the received logical block data followed by the received Guard field.

**5.3.1.3.2**

**64b CRC Generation**
The equations that are used to generate the 64b CRC from F(x) are as follows. All arithmetic is modulo 2.
The transmitter shall calculate the 64b CRC by appending 64 bits of zeroes to F(x) and dividing by G(x) to
obtain the remainder R(x):
(𝑥64 × 𝐹(𝑥))
𝐺(𝑥)
= 𝑄𝐴(𝑥) +
𝑅(𝑥)
𝐺(𝑥)

R(x) is the 64b CRC value, and is transmitted in the Guard field.
M(x) is the polynomial representing the logical block data followed by the Guard field (i.e., F(x) followed by
R(x)):
𝑀(𝑥) = (𝑥64 × 𝐹(𝑥)) + 𝑅(𝑥)

**5.3.1.3.3**

**64b CRC Checking**
M’(x) (i.e., the polynomial representing the received logical block data followed by the received Guard field)
may differ from M(x) (i.e., the polynomial representing the transmitted logical block data followed by the
transmitted Guard field) if there are transmission errors.
The receiver may check M’(x) validity by appending 64 bits of zeroes to F’(x) and dividing by G(x) and
comparing the calculated remainder RB(x) to the received CRC value R’(x):
(𝑥64 × 𝐹′(𝑥))
𝐺(𝑥)
= 𝑄𝐵(𝑥) +
𝑅𝐵(𝑥)
𝐺(𝑥)

In the absence of errors in F’(x) and R’(x), the remainder RB(x) is equal to R’(x).
The receiver may check M’(x) validity by dividing M’(x) by G(x) and comparing the calculated remainder
RC(x) to zero:

𝑀′(𝑥)
𝐺(𝑥) = 𝑄𝐶(𝑥) +
𝑅𝐶(𝑥)
𝐺(𝑥)

In the absence of errors in F’(x) and R’(x), the remainder RC(x) is equal to zero.
Both methods of checking M’(x) validity are mathematically equivalent.

**5.3.1.3.4**

**RocksoftTM Model CRC Algorithm parameters for 64b CRC**
The 64-bit CRC required by this specification uses the generator polynomial AD93D235_94C93659h. The
64-bit CRC is calculated using the Rocksoft Model CRC Algorithm parameters defined in Figure 153.


||Function|||Definition||
|---|---|---|---|---|---|
|QB(x)|||The quotient polynomial calculated during CRC checking by the receiver.<br>The value of QB(x) is not used.|||
|QC(x)|||The quotient polynomial calculated during CRC checking by the receiver.<br>The value of QC(x) is not used.|||
|M(x)|||A polynomial representing the transmitted logical block data followed by the transmitted Guard field.|||
|M’(x)|||A polynomial representing the received logical block data followed by the received Guard field.|||

134

**Figure 153: 64-bit CRC Rocksoft Model Parameters**

**Parameter**

**Value**
Name
“NVM Express 64b CRC”
Width
Poly
AD93D235_94C93659h
Init
FFFFFFFF_FFFFFFFFh
RefIn
True
RefOut
True
XorOut
FFFFFFFF_FFFFFFFFh
Check
11199E50_6128D175h

When sending a logical block and metadata, the 64b Guard field shall be calculated using the following
procedure or a procedure that produces an equivalent result:
1. Initialize the CRC register to FFFFFFFF_FFFFFFFFh. This is equivalent to inverting the lowest 64
bits of the user data;
2. Append 64 bits of 0’s to the end of each logical block and metadata not including the 64b Protection
Information. This results in the Guard field shown in Figure 151 to be cleared to 0h;
3. Map the bits from step 2 to the coefficients of the message polynomial M(x). Assume the length of
M(x) is Y bytes. Bit 0 of byte 0 in the logical block is the most significant bit of M(x), followed by bit
1 of byte 0, on through to bit 7 of byte Y - 1. Note that the bits within each byte are reflected (i.e.,
bit n of each byte is mapped to bit (7 - n) resulting in bit 7 to bit 0, bit 6 to bit 1, and so on);

**Figure 154: Logical Block and Metadata Example**

**Message Body (Length = Y bytes)**

**Byte 0**

**Byte 1**

**…**

**Byte Y - 1**
M(x) =
…

4. Divide the polynomial M(x) by the generator polynomial AD93D235_94C93659h to produce the 64-
bit remainder polynomial R(x);
5. Reflect each byte of R(x) (i.e., bit n of each byte is mapped to bit (7 - n) resulting in bit 7 to bit 0, bit
6 to bit 1, and so on) to produce the polynomial R′(x);
6. Invert R′(x) to produce the polynomial R′′(x); and
7. Store R′′(x) in the 64b Guard field in the 64b Protection Information.
Upon receipt of a logical block and metadata, the Guard field may be validated as follows:
1. Save the received Guard field;
2. Initialize the CRC register to FFFFFFFF_FFFFFFFFh. This is equivalent to inverting the lowest 64
bits of the logical block;
3. Clear the Guard field to 0h;
4. Map the bits in the logical block and metadata excluding the protection information to the
coefficients of the message polynomial M(x) as described in step 3 in the Guard field calculation
procedure for sending a logical block and metadata;
5. Divide the polynomial M(x) by the generator polynomial AD93D235_94C93659h to produce the 64-
bit remainder polynomial R(x);
6. Reflect each byte of R(x) (i.e., bit n of each byte is mapped to bit (7 - n) resulting in bit 7 to bit 0, bit
6 to bit 1, and so on) to produce the polynomial R′(x);
7. Invert R′(x) to produce the polynomial R′′(x); and
8. Compare R′′(x) from step 7 to the Guard field value saved in step 1. If both values are equal, the
64b CRC check passes.


||Figure 153: 64-bit CRC Rocksoft Model Parameters|||||
|---|---|---|---|---|---|
||Parameter|||Value||
|Name|||“NVM Express 64b CRC”|||
|Width|||64|||
|Poly|||AD93D235 94C93659h|||
|Init|||_<br>FFFFFFFF FFFFFFFFh|||
|RefIn|||_<br>True|||
|RefOut|||True|||
|XorOut|||FFFFFFFF FFFFFFFFh|||
|Check|||_<br>11199E50 6128D175h|||


||Message Body (Length = Y bytes)||||||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Byte 0||||||||||Byte 1||||||||||…|||Byte Y - 1|||||||||
|0||1|2|3|4|5|6|7||0||1|2|3|4|5|6|7||…|||0||1|2|3|4|5|6|7||

135

**5.3.1.3.5**

**64b CRC Test Cases**
Several 64b CRC test cases are shown in Figure 155.

**Figure 155: 64b CRC Test Cases for 4 KiB Logical Block with no Metadata**

**Logical Block Contents**

**64b Guard Field Value**
4 KiB bytes each byte cleared to 00h
6482D367_EB22B64Eh
4 KiB bytes each byte set to FFh
C0DDBA73_02ECA3ACh
4 KiB bytes of an incrementing byte pattern from 00h to FFh,
repeating (e.g., byte 0 is set to 00h, byte 1 is set to 01h, … , byte
254 is set to FEh, byte 255 is set to FFh, byte 256 is set to 00h,
…)
3E729F5F_6750449Ch

4 KiB bytes of a decrementing pattern from FFh to 00h, repeating
(e.g., byte 0 is set to FFh, byte 1 is set to FEh, … , byte 254 is set
to 01h, byte 255 is set to 00h, byte 256 is set to FFh, …)
9A2DF64B8_E9E517Eh

**5.3.1.4**

**Storage Tag and Logical Block Reference Tag from Storage and Reference Space**
The Storage Tag Size (STS) field in the Identify Namespace data structure allows the separation of the
Storage and Reference Space field in the protection information into a Storage Tag field and a Logical
Block Reference Tag field as shown in Figure 156. If the STS field value is 0h, then no Storage Tag field is
defined for the 16b Guard Protection Information and 64b Guard Protection Information formats. If the STS
field value is non-zero, then that value specifies the number of most significant bits of the Storage and
Reference Space field that is the Storage Tag field. The remaining least significant bits of the Storage and
Reference Space field, if any, specify the Logical Block Reference Tag field. If the STS field value is equal
to the size of the Storage and Reference Space field, then no Logical Block Reference Tag field is defined.

**Figure 156: Separation of Storage and Reference Space into Storage Tag and Logical Block**

**Reference Tag**

Reference Tag
Storage Tag
Storage and Reference Space
Storage Tag Size

Most Significant Bits
Least Significant Bits

**5.3.1.4.1**

**Storage Tag Field and Logical Block Reference Tag Field**
For I/O commands processed on namespaces with end-to-end protection enabled, the checking of the
Storage Tag field, if defined, and the Logical Block Reference Tag requires variable sized Logical Block
Storage Tag (LBST) field, Expected Logical Block Storage Tag (ELBST) field, Initial Logical Block
Reference Tag (ILBRT) field, and Expected Initial Logical Block Reference Tag (EILBRT) field. This section
defines the layout of these variable fields in Command Dword 2, Command Dword 3, and Command Dword


||Figure 155: 64b CRC Test Cases for 4 KiB Logical Block with no Metadata|||||
|---|---|---|---|---|---|
||Logical Block Contents|||64b Guard Field Value||
|4 KiB bytes each byte cleared to 00h|||6482D367 EB22B64Eh|||
|4 KiB bytes each byte set to FFh|||_<br>C0DDBA73 02ECA3ACh|||
|4 KiB bytes of an incrementing byte pattern from 00h to FFh,<br>repeating (e.g., byte 0 is set to 00h, byte 1 is set to 01h, … , byte<br>254 is set to FEh, byte 255 is set to FFh, byte 256 is set to 00h,<br>…)|||_<br>3E729F5F 6750449Ch<br>_|||
|4 KiB bytes of a decrementing pattern from FFh to 00h, repeating<br>(e.g., byte 0 is set to FFh, byte 1 is set to FEh, … , byte 254 is set<br>to 01h, byte 255 is set to 00h, byte 256 is set to FFh, …)|||9A2DF64B8 E9E517Eh<br>_|||


||||
|---|---|---|
||||
|||Storage and Reference Space|
|Most Significant Bits<br>Storage Tag||Least Significant Bits<br>Reference Tag|

136
14. Figure 157 shows the minimum and maximum sizes of the LBST, ELBST, ILBRT and EILBRT fields
based on the value of the Storage Tag Size (STS) field (refer to Figure 119) for each protection information
format (refer to section 5.3.1).

**Figure 157: LBST and LBRT Minimum and Maximum Sizes**

**STS Value**

**LBST/ELBST**

**Bit Size**

**ILBRT/EILBRT**

**Bit Size**

**16b Guard Protection Information**

**32b Guard Protection Information**

**64b Guard Protection Information**

Note:
1.
Storage Tag field is not defined.
2.
Logical Block Reference Tag field is not defined.

Figure 158 shows the layout of the LBST/ELBST and ILBRT/ EILBRT fields in Command Dword 2,
Command Dword3, and Command Dword 14.
16b Guard Protection Information and 64b Guard Protection Information do not require the 80 bits allocated
for the LBST, ELBST, ILBRT, and EILBRT fields in CDW 2, CDW 3, and CDW 14. Any unused bits are
ignored by the controller (i.e., for 16b Guard Protection Information CDW2 and CDW 3 are ignored). If STS
field value is 0h, then the Storage Tag field is not defined and the LBST and ELBST fields are not defined.


|STS Value|||LBST/ELBST|||ILBRT/EILBRT||
|---|---|---|---|---|---|---|---|
||||Bit Size|||Bit Size||
||16b Guard Protection Information|||||||
|0||1<br>0|||32|||
|32||32|||2<br>0|||
||32b Guard Protection Information|||||||
|16||16|||64|||
|64||64|||16|||
||64b Guard Protection Information|||||||
|0||1<br>0|||48|||
|48||48|||2<br>0|||
|Note:<br>1. Storage Tag field is not defined.<br>2. Logical Block Reference Tag field is not defined.||||||||

137

**Figure 158: LBST, ELBST, ILBRT, and EILBRT fields Format in Command Dwords**

Figure 159 shows the layout of the LBST, ELBST, ILBRT, and EILBRT fields for I/O commands that utilize
the fields.

**Figure 159: I/O Command LBST, ELBST, ILBRT, and EILBRT fields Format**

**Bits**

**Description**

**16b Guard Protection Information**

**Command Dword 2**
15:00
Ignored by the controller

**Command Dword 3**
31:00
Ignored by the controller

**Command Dword 14**
31:00
Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158

**32b Guard Protection Information**

**Command Dword 2**
15:00
Most significant bit of the LBST or ELBST

**Command Dword 3**
31:00
Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158

**Command Dword 14**
31:00
Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158

**64b Guard Protection Information**

**Command Dword 2**
15:00
Ignored by the controller

**Command Dword 3**
31:16
Ignored by the controller
15:00
Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158

**Command Dword 14**
31:00
Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158


||Bits|||Description||
|---|---|---|---|---|---|
||16b Guard Protection Information|||||
||Command Dword 2|||||
|15:00|||Ignored by the controller|||
||Command Dword 3|||||
|31:00|||Ignored by the controller|||
||Command Dword 14|||||
|31:00|||Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158|||
||32b Guard Protection Information|||||
||Command Dword 2|||||
|15:00|||Most significant bit of the LBST or ELBST|||
||Command Dword 3|||||
|31:00|||Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158|||
||Command Dword 14|||||
|31:00|||Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158|||
||64b Guard Protection Information|||||
||Command Dword 2|||||
|15:00|||Ignored by the controller|||
||Command Dword 3|||||
|31:16|||Ignored by the controller|||
|15:00|||Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158|||
||Command Dword 14|||||
|31:00|||Variable sized LBST, ELBST, ILBRT or EILBRT as defined in Figure 158|||

138
For an example of the 16b Guard Protection Information usage of Command Dword 2, Command Dword
3, and Command Dword 14 assume a namespace is formatted with the following:
a) LBA Data Size field (refer to Figure 116) cleared to 0h specifying a 512B logical block data size;
b) Metadata Size field (refer to Figure 116) set to 8h specifying an 8B metadata size;
c) Protection Information Format field (refer to Figure 118) cleared to 00b specifying the 16b Guard
Protection Information; and
d) Storage Tag Size (STS) field (refer to Figure 119) cleared to 0h specifying that the Storage and
Reference Space field is the Logical Block Reference Tag (i.e., the Storage Tag field is not defined),
then the definition of Command Dword 2, Command Dword 3, and Command Dword 14 for a Write
command is shown in Figure 160 and for a Read command is shown in Figure 161.

**Figure 160: 16b Guard Protection Information Write Command Example**

**Bits**

**Description**

**Command Dword 2**
15:00
Ignored by the controller

**Command Dword 3**
31:00
Ignored by the controller

**Command Dword 14**
31:00
ILBRT

**Figure 161: 16b Guard Protection Information Read Command Example**

**Bits**

**Description**

**Command Dword 2**
15:00
Ignored by the controller

**Command Dword 3**
31:00
Ignored by the controller

**Command Dword 14**
31:00
EILBRT

For an example of the 32b Guard Protection Information usage of Command Dword 2, Command Dword
3, and Command Dword 14 assume a namespace is formatted with the following:
a) LBA Data Size field (refer to Figure 116) set to Ch specifying a 4 KiB logical block data size;
b) Metadata Size field (refer to Figure 116) set to 10h specifying a 16B metadata size;
c) Protection Information Format field (refer to Figure 118) set to 01b specifying the 32b Guard
Protection Information; and
d) Storage Tag Size (STS) field (refer to Figure 119 set to 20h specifying that the most significant 32
bits of the Storage and Reference Space field are the Storage Tag field,
then the definition of Command Dword 2, Command Dword 3, and Command Dword 14 for a Write
command is shown in Figure 162 and for a Read command is shown in Figure 163.

**Figure 162: 32b Guard Protection Information Write Command Example**

**Bits**

**Description**

**Command Dword 2**
15:00
Most significant 16 bits of the LBST

**Command Dword 3**
31:16
Least significant 16 bits of LBST
15:00
Most significant 16 bits of the ILBRT


||Bits|||Description||
|---|---|---|---|---|---|
||Command Dword 2|||||
|15:00|||Ignored by the controller|||
||Command Dword 3|||||
|31:00|||Ignored by the controller|||
||Command Dword 14|||||
|31:00|||ILBRT|||


||Bits|||Description||
|---|---|---|---|---|---|
||Command Dword 2|||||
|15:00|||Ignored by the controller|||
||Command Dword 3|||||
|31:00|||Ignored by the controller|||
||Command Dword 14|||||
|31:00|||EILBRT|||


||Bits|||Description||
|---|---|---|---|---|---|
||Command Dword 2|||||
|15:00|||Most significant 16 bits of the LBST|||
||Command Dword 3|||||
|31:16|||Least significant 16 bits of LBST|||
|15:00|||Most significant 16 bits of the ILBRT|||

139

**Figure 162: 32b Guard Protection Information Write Command Example**

**Bits**

**Description**

**Command Dword 14**
31:00
Least significant 32 bits of ILBRT

**Figure 163: 32b Guard Protection Information Read Command Example**

**Bits**

**Description**

**Command Dword 2**
15:00
Most significant 16 bits of the ELBST

**Command Dword 3**
31:00
Least significant 16 bits of ELBST
15:00
Most significant 16 bits of EILBRT

**Command Dword 14**
31:00
Least significant 32 bits of EILBRT

For an example of the 64b Guard Protection Information usage of Command Dword 2, Command Dword
3, and Command Dword 14 assume a namespace is formatted with the following:
a) LBA Data Size field (refer to Figure 116) set to Ch specifying a 4 KiB logical block data size;
b) Metadata Size field (refer to Figure 116) set to 10h specifying a 16B metadata size;
c) Protection Information Format field (refer to Figure 118) set to 10b specifying the 64b Guard
Protection Information; and
d) Storage Tag Size (STS) field (refer to Figure 119) set to 12h specifying that the most significant 18
bits of the Storage and Reference Space field are the least significant 18 bits of the Storage Tag field,
then the definition of Command Dword 2, Command Dword 3, and Command Dword 14 for a Write
command is shown in Figure 164 and for a Read command is shown in Figure 165.

**Figure 164: 64b Guard Protection Information Write Command Example**

**Bits**

**Description**

**Command Dword 2**
15:00
Ignored by the controller

**Command Dword 3**
31:16
Ignored by the controller
15:00
Most significant 16 bits of LBST

**Command Dword 14**
31:30
Least significant 2 bits of LBST
29:00
ILBRT

**Figure 165: 64b Guard Protection Information Read Command Example**

**Bits**

**Description**

**Command Dword 2**
15:00
Ignored by the controller

**Command Dword 3**
31:16
Ignored by the controller
15:00
Most significant 16 bits of the ELBST

**Command Dword 14**
31:30
Least significant 2 bits of ELBST
29:00
EILBRT


||Bits|||Description||
|---|---|---|---|---|---|
||Command Dword 14|||||
|31:00|||Least significant 32 bits of ILBRT|||


||Bits|||Description||
|---|---|---|---|---|---|
||Command Dword 2|||||
|15:00|||Most significant 16 bits of the ELBST|||
||Command Dword 3|||||
|31:00|||Least significant 16 bits of ELBST|||
|15:00|||Most significant 16 bits of EILBRT|||
||Command Dword 14|||||
|31:00|||Least significant 32 bits of EILBRT|||


||Bits|||Description||
|---|---|---|---|---|---|
||Command Dword 2|||||
|15:00|||Ignored by the controller|||
||Command Dword 3|||||
|31:16|||Ignored by the controller|||
|15:00|||Most significant 16 bits of LBST|||
||Command Dword 14|||||
|31:30|||Least significant 2 bits of LBST|||
|29:00|||ILBRT|||


||Bits|||Description||
|---|---|---|---|---|---|
||Command Dword 2|||||
|15:00|||Ignored by the controller|||
||Command Dword 3|||||
|31:16|||Ignored by the controller|||
|15:00|||Most significant 16 bits of the ELBST|||
||Command Dword 14|||||
|31:30|||Least significant 2 bits of ELBST|||
|29:00|||EILBRT|||

140

**5.3.1.4.2**

**Host Considerations when Formatting with Storage Tag (Informative)**
The Format NVM command does not provide a method to change the Storage Tag Size (STS) field of the
LBA format that a namespace is formatted with:
•
from the value 0h to a non-zero value; or
•
from a non-zero value to a different non-zero value.
The Namespace Management command, if supported, is able to be used to delete the existing namespace
and to create a namespace with a different combination of values in the Storage Tag Size (STS) field and
the Logical Block Storage Tag Mask (LBSTM) field.

**PRACT Bit**
The protection information processing performed as a side effect of Read and Write commands is controlled
by the Protection Information Action (PRACT) bit in the command.

**5.3.2.1**

**Protection Information and Write Commands**
Figure 166 provides some examples of the protection information processing that may occur as a side effect
of a Write command.
If the namespace is not formatted with end-to-end data protection, then logical block data and metadata is
transferred from the host to the NVM with no protection information related processing by the controller.
If the namespace is formatted with protection information and the PRACT bit is cleared to ‘0’, then logical
block data and metadata, which contains the protection information and may contain additional metadata,
are transferred from the host buffer to NVM (i.e., the metadata field remains the same size in the NVM and
the host buffer). As the logical block data and metadata passes through the controller, the protection
information is checked. If a protection information check error is detected, the command completes with the
status code of the error detected (i.e., End-to-end Guard Check Error, End-to-end Application Tag Check
Error, End-to-end Storage Tag Check Error, or End-to-end Reference Tag Check Error).
If the namespace is formatted with protection information and the PRACT bit is set to ‘1’, then:
1. If the namespace is formatted with Metadata Size (refer to Figure 116) equal to protection
information size (refer to section 5.3.1), then the logical block data is transferred from the host
buffer to the controller. As the logical block data passes through the controller, the controller
generates and appends protection information to the end of the logical block data, the PRCHK field
settings and the STC bit settings are ignored, and the logical block data and protection information
are written to NVM (i.e., the metadata is not resident within the host buffer); and
2. If the namespace is formatted with Metadata Size greater than protection information size, then the
logical block data and the metadata are transferred from the host buffer to the controller. As the
metadata passes through the controller, the controller overwrites the protection information portion
of the metadata without checking the protection information portion regardless of the PRCHK field
settings and regardless of the STC bit setting. The logical block data and metadata are written to
the NVM (i.e., the metadata field remains the same size in the NVM and the host buffer). The
location of the protection information within the metadata is configured when the namespace is
formatted (refer to the DPS field in Figure 114).
141

**Figure 166: Write Command 16b Guard Protection Information Processing**

**5.3.2.2**

**Protection Information and Read Commands**
Figure 167 provides some examples of the protection information processing that may occur as a side effect
of Read command processing.
If the namespace is formatted with protection information and the PRACT bit is cleared to ‘0’, then the
logical block data and metadata, which in this case contains the protection information and possibly
a) MD=8, PRACT=0: Metadata remains same size in NVM and host buffer

b) MD>8 (e.g., 16), PI, PRACT=0: Metadata remains same size in NVM and host buffer

c) MD=8, PI, PRACT=1: Metadata not resident in host buffer

d) MD>8 (e.g., 16), PI, PRACT=1: Metadata remains same size in NVM and host buffer
142
additional host metadata, is transferred by the controller from the NVM to the host buffer (i.e., the metadata
field remains the same size in the NVM and the host buffer). As the logical block data and metadata pass
through the controller, the protection information within the metadata is checked. If a protection information
check error is detected, the command completes with the status code of the error detected (i.e., End-to-
end Guard Check Error, End-to-end Application Tag Check Error, End-to-end Storage Tag Check Error, or
End-to-end Reference Tag Check Error).
If the namespace is formatted with protection information and the PRACT bit is set to ‘1’, then:
a) If the namespace is formatted with Metadata Size (refer to Figure 116) equal to protection
information size (refer to section 5.3.1), the logical block data and metadata (which in this case is,
by definition, the protection information) is read from the NVM by the controller. As the logical block
and metadata pass through the controller, the protection information is checked. If a protection
information check error is detected, the command completes with the status code of the error
detected (i.e., End-to-end Guard Check Error, End-to-end Application Tag Check Error, End-to-end
Storage Tag Check Error, or End-to-end Reference Tag Check Error). After processing the
protection information, the controller only returns the logical block data to the host (i.e., the
metadata is not resident within the host buffer); and
b) if the namespace is formatted with Metadata Size greater than protection information size, the
logical block data and the metadata, which in this case contains the protection information and
additional host formatted metadata, is read from the NVM by the controller. As the logical block and
metadata pass through the controller, the protection information embedded within the metadata is
checked. If a protection information check error is detected, the command completes with the status
code of the error detected (i.e., End-to-end Guard Check Error, End-to-end Application Tag Check
Error, End-to-end Storage Tag Check Error, or End-to-end Reference Tag Check Error). After
processing the protection information, the controller passes the logical block data and metadata,
with the embedded protection information unchanged, to the host (i.e., the metadata field remains
the same size in the NVM as within the host buffer).
143

**Figure 167: Read 16b Guard Command Protection Information Processing**

**5.3.2.3**

**Protection Information for Fused Operations**
Protection processing for fused operations is the same as those for the individual commands that make up
the fused operation.
144

**5.3.2.4**

**Protection Information and Compare commands**
Figure 168 illustrates the protection information processing that may occur as a side effect of Compare
command processing. Compare command processing parallels both Write and Read commands. For the
portion of the Compare command that transfers data and protection information from the host to the
controller, the protection information checks performed by the controller parallels the Write command
protection information checks (refer to section 5.3.2.1). For the portion of the Compare command that
transfers data and protection information from the NVM media to the controller, the protection information
checks performed by the controller parallels the Read command protection information checks (refer to
section 5.3.2.2). The ELBST, EILBRT, PRINFO, STC, ELBATM, and ELBAT fields in the command are
used by both sets of protection information checks as defined in section 5.3.3.

**Figure 168: Protection Information Processing for Compare**

**5.3.2.5**

**Protection Information and Copy commands**
Protection information (PI) processing during a Copy command parallels both Write and Read commands.
For the portion of the Copy command that transfers data and PI from the LBAs described by a Source
Range entry (refer to Figure 39 and Figure 40), the PI checks performed by the controller are controlled by
the PRINFOR field in Copy command Dword 12 (refer to Figure 34) and parallels the Read command PI
checks (refer to section 5.3.2.2) as follows:
•
The logical block data and metadata is transferred from the NVM to the controller.
•
As the logical block data and metadata pass through the controller, the PI within the metadata is
checked. If a PI check error is detected, the command completes with the status code of the error
detected (i.e., End-to-end Guard Check Error, End-to-end Application Tag Check Error, End-to-end
Storage Tag Check Error, or End-to-end Reference Tag Check Error).
For the portion of the Copy command that transfers data and PI to the LBAs starting at the SDLBA field
(refer to Figure 33), the PI operations performed by the controller are controlled by the PRINFOW field in
Copy command Dword 12 (refer to Figure 34) and parallels the Write command PI checks (refer to section
5.3.2.1) as follows:
•
The logical block data and metadata are transferred from the controller to the NVM.
•
As the logical block data and metadata passes through the controller, the PI is handled as described
in section 5.3.2.1.
145

**Figure 169: PI Processing for Copy MD=8 Pass-through**

Copy
Command

**NVM**

MD=8, PI, PRINFOR.PRACT=PRINFOW.PRACT=0 : PI pass-through

**CTLR**
LB Data

PI
LB Data
Source 1

MD=8
Source 0

Destination
PI
MD=8

**Figure 170: PI Processing for Copy MD=16 Pass-through**

Copy
Command

**NVM**

MD=16, PI, PRINFOR.PRACT=PRINFOW.PRACT=0 : PI pass-through

**CTLR**
LB Data

LB Data
Source 1
Source 0

Destination
PI
MD

PI
MD
MD=16

MD=16
146

**Figure 171: PI Processing for Copy MD=8 Replace**

Copy
Command

**NVM**

MD=8, PI, PRINFOR.PRACT=PRINFOW.PRACT=1 : PI replace

**CTLR**
LB Data

PI
LB Data
Source 1

MD=8
Source 0

Destination
PI
MD=8

**Figure 172: PI Processing for Copy MD=16 Replace**

Copy
Command

**NVM**

MD=16, PI, PRINFOR.PRACT=PRINFOW.PRACT=1 : PI replace

**CTLR**
LB Data

LB Data
Source 1
Source 0

Destination
PI
MD

PI
MD
MD=16

MD=16
147

**Figure 173: PI Processing for Copy MD=8 Insert**

Copy
Command

**NVM**

destination MD=8, PI, PRINFOW.PRACT=1: PI insert

**CTLR**
LB Data

PI
LB Data
Source 1

MD=8
Source 0

Destination

**Figure 174: PI Processing for Copy MD=8 Strip**

Copy
Command

**NVM**

source MD=8, PI, PRINFOR.PRACT=1: PI strip

**CTLR**
LB Data
PI

LB Data
Source 1
MD=8

Source 0

Destination

Figure 169, Figure 170, Figure 171, Figure 172, Figure 173, and Figure 174 shows six examples of PI
processing for the Copy command where the Copy command in each example copies from two source
regions in two different source namespaces to a destination region in a third destination namespace.
While user data is passing through the controller the data should never be unprotected (e.g., Calculate the
PI data associated with the write portion of the copy operation occurs before verification and removal of PI
data associated with the read portion of the copy operation). If the Guard field is recalculated, then that
Guard field should be compared to the original Guard field (i.e., the Guard field associated with the read
portion of the copy operation).
148

**5.3.2.5.1**

**Protection Information and copying within the same namespace**
If a Copy command uses Source Range Entries Copy Descriptor Format 0h or 1h to request that user data
in a Source Range be copied to the same namespace and that namespace is formatted with protection
information (PI), then that user data is copied only if the PRINFOR.PRACT bit and the PRINFOW.PRACT
bit in the Copy command have the same value (refer to section 3.3.2.3):
•
If the PRINFOR.PRACT bit and the PRINFOW.PRACT bit are both set to ‘1’, then as the logical
block data and metadata pass through the controller, the PI is replaced with PI that is generated
by the controller as shown for the examples in Figure 169 and Figure 170; and
•
If the PRINFOR.PRACT bit and the PRINFOW.PRACT bit are both cleared to ‘0’, then the logical
block data and metadata pass through the controller without change to the PI as shown for the
examples in Figure 171 and Figure 172.
If the PRINFOR.PRACT bit and the PRINFOW.PRACT bit do not have the same value, then the Copy
command is aborted with a status code of Invalid Field in Command (refer to section 3.3.2.3).
PI checks for copied user data are performed as described in section 5.3.2.5.

**5.3.2.5.2**

**Protection Information and copying across different namespaces**
This section applies to Copy commands that use either Source Range Entries Copy Descriptor format 2h
or 3h to copy data across multiple namespaces and/or within the same namespace. Refer to section
5.3.2.5.1 for Copy commands that use Source Range Entries Copy Descriptor Format 0h or 1h.
Controller processing of protection information (PI) as part of a copy operation depends on the format of
the destination namespace, the format of each source namespace and the values of the PRINFOR.PRACT
bit and the PRINFOW.PRACT bit in the Copy command.
If the destination namespace and a source namespace are both formatted with PI and the two namespaces
have matching namespace formats for copy (refer to section 3.3.2.4.1), then:
•
if the PRINFOR.PRACT bit and the PRINFOW.PRACT bit are both set to ‘1’, then as the logical
block data and metadata pass through the controller, the PI is overwritten with PI that is generated
by the controller as shown for the examples in Figure 169 and Figure 170; and
•
if the PRINFOR.PRACT bit and the PRINFOW.PRACT bit are both cleared to ‘0’ then the logical
block data and metadata pass through the controller without change as shown for the examples in
Figure 171 and Figure 172.
All other cases in which the destination namespace and a source namespace are both formatted with PI
result in the controller aborting the Copy command with an error status (refer to section 3.3.2.4.2).
If the destination namespace is formatted with PI, a source namespace is formatted without PI, and:
•
the two namespaces have corresponding PI formats for copy (refer to section 3.3.2.4.1); and
•
the PRINFOW.PRACT bit is set to ‘1’,
then as the logical block data passes through the controller, the controller generates and appends PI to the
end of the logical block data as shown for the example in Figure 173. All other cases in which the destination
namespace is formatted with PI and a source namespace is formatted without PI result in the controller
aborting the Copy command with an error status (refer to section 3.3.2.4.2), including cases where the
metadata size of the destination namespace is larger than the PI size of that namespace.
If the destination namespace is formatted without PI, a source namespace is formatted with PI, and:
149
•
the two namespaces have corresponding PI formats for copy; and
•
the PRINFOR.PRACT bit is set to ‘1’,
then as the logical block data and metadata pass through the controller, the PI is stripped, and the controller
only writes the logical block data to the NVM as shown for the example in Figure 174. All other cases in
which the destination namespace is formatted without PI and a source namespace is formatted with PI
result in the controller aborting the Copy command with an error status (refer to section 3.3.2.4.2), including
cases where the metadata size of a source namespace is larger than the PI size of that namespace.
PI checks for copied user data are performed as described in section 5.3.2.5.

**Control of Protection Information Checking - PRCHK**
Checking of protection information consists of the following operations performed by the controller.
•
If the Guard Check bit of the Protection Information Check (PRCHK) field of the command is set to
‘1’, then the controller compares the protection information Guard field to the CRC for the protection
information format (refer to section 5.3.1) computed over the logical block data.
•
If the Application Tag Check bit of the PRCHK field is set to ‘1’, then the controller compares
unmasked bits in the protection information Application Tag field to the Logical Block Application
Tag (LBAT) field in the command. A bit in the protection information Application Tag field is masked
if the corresponding bit is cleared to ‘0’ in the Logical Block Application Tag Mask (LBATM) field of
the command or the Expected Logical Block Application Tag Mask (ELBATM) field. If a Storage
Tag field is defined in the protection information (refer to section 5.3.1.4) and the Storage Tag
Check bit in the command is set to ‘1’, then the controller compares unmasked bits in the Storage
Tag field to the Logical Block Storage Tag (LBST) field of the command. A bit in the Storage Tag
field is masked (i.e., not compared) if the corresponding bit is cleared to ‘0’ in the Logical Block
Storage Tag Mask (LBSTM) field in the NVM Command Set Identify Namespace data structure
(refer to Figure 118). Implementations may limit support for the bits that are allowed to be masked
in the Logical Block Storage Tag Mask as described in the Storage Tag Masking Level Attribute
field (refer to Figure 118).
•
If the Reference Tag is defined (refer to Figure 119) then:
o
If the Reference Tag Check bit of the PRCHK field is set to ‘1’ and the namespace is
formatted for Type 1 or Type 2 protection, then the controller compares the Logical Block
Reference Tag to the computed reference tag. The computed reference tag depends on
the Protection Type:
▪
If the namespace is formatted for Type 1 protection, the value of the computed
reference tag for the first logical block of the command is the value contained in
the Initial Logical Block Reference Tag (ILBRT) or Expected Initial Logical Block
Reference Tag (EILBRT) field in the command, and the computed reference tag is
incremented for each subsequent logical block. The controller shall complete the
command with a status of Invalid Protection Information if the ILBRT field or the
EILBRT field does not match the value of the least significant bits of the SLBA field
sized to the number of bits in the Logical Block Reference Tag (refer to section
5.3.1.4).
Note: Unlike SCSI Protection Information Type 1 protection which implicitly uses
the least significant four bytes of the LBA, the controller always uses the ILBRT or
EILBRT field and requires the host to initialize the ILBRT or EILBRT field to the
150
least significant bits of the LBA sized to the number of bits in the Logical Block
Reference Tag when Type 1 protection is used.
▪
If the namespace is formatted for Type 2 protection, the value of the computed
reference tag for the first logical block of the command is the value contained in
the Initial Logical Block Reference Tag (ILBRT) or Expected Initial Logical Block
Reference Tag (EILBRT) field in the command, and the computed reference tag is
incremented for each subsequent logical block.
o
If the Reference Tag Check bit of the PRCHK field is set to ‘1’ and the namespace is
formatted for Type 3 protection, then the controller:
▪
should not compare the protection Information Reference Tag field to the
computed reference tag; and
▪
may ignore the ILBRT and EILBRT fields. If a command is aborted as a result of
the Reference Tag Check bit of the PRCHK field being set to ‘1’, then that
command shall be aborted with a status code of Invalid Protection Information.
o
Incrementing a computed reference tag with all bits set to ‘1’ produces a value with all bits
cleared to ‘0’ (i.e., the computed reference tag rolls over to 0h).
Protection checking may be disabled as a side effect of the value of the protection information Application
Tag and Logical Block Reference Tag, if defined, regardless of the state of the PRCHK field and the Storage
Tag Check (STC) field in the command. If the namespace is formatted for Type 1 or Type 2 protection, then
all protection information checks are disabled regardless of the state of the PRCHK field and the STC field
when the protection information Application Tag has a value of FFFFh.
If the namespace is formatted for Type 3 protection, then all protection information checks are disabled
regardless of the state of the PRCHK field and the STC field when the protection information Application
Tag and Logical Block Reference Tag, if defined, have all bits set to ‘1’.
Inserted protection information consists of the computed CRC for the protection information format (refer to
section 5.3.1) in the Guard field, the LBAT field value in the Application Tag field, the LBST field value in
the Storage Tag field, if defined, and the computed reference tag in the Logical Block Reference Tag.

**5.4**

**Key Per I/O**

The Key Per I/O capability operates as defined by the NVM Express Base Specification with the exceptions
specified by this section. The Trusted Computing Group Security Subsystem Key Per I/O specification
makes use of this NVM Express capability.
Any I/O command specifying the key tag (i.e., CETYPE value of KPIOTAG) that does not have:
a) the SLBA field in that command aligned on a logical block boundary specified by the KPIODAAG
field in the Identify Namespace data structure (refer to Figure 114); and
b) the range of LBAs accessed by that command specify a granularity specified by the KPIODAAG
field,
then the controller shall abort that command with a status code of Invalid Field in Command.

**5.5**

**LBA Format List Structure**

To create or format a namespace, a host specifies an LBA Format (i.e., the Format Index) referencing the
LBA Format list in the NVM Command Set Identify Namespace data structure. The LBA Format list has a
structure as is illustrated in Figure 175. The NLBAF field, a 0-based number (i.e., at least one is required
151
to be defined), identifies the number of LBA Formats that have the same capabilities used to format and
create a namespace (i.e., the green LBA Formats). The Identify command provides the ability to access
these same capabilities in a namespace data structure by specifying an NSID of FFFFFFFFh.
The NULBAF field, a 1-based number (i.e., none may be defined), identifies the number of LBA Formats
that have unique attributes (i.e., that may not be the same capabilities as other LBA Formats) used to format
and create a namespace (i.e., the orange LBA Formats). A host should use the Identify command with a
CNS value of 09h to access the capabilities of a specific LBA Format for the NVM Command Set Identify
Namespace data structure. A host should use the Identify command with a CNS value of 0Ah to access the
capabilities of a specific LBA Format for an I/O Command Set specific Identify Namespace data structure
for the NVM Command Set.
Figure 176 shows the association of CNS values of the Identify command that provides the ability to access
these same capabilities to specific LBA Format entries referenced by the NLBAF field and NULBF field.
The maximum number of LBA formats allowed to be supported is:
•
16 if the LBA Format Extension Enable (LBAFEE) field is cleared to 0h in the Host Behavior Support
feature (refer to the Host Behavior Support section in the NVM Express Base Specification); or
•
64 if the LBAFEE field is set to 1h in the Host Behavior Support feature (refer to the Host Behavior
Support section in the NVM Express Base Specification).
The total number of LBA formats supported is the sum of the values represented by the NLBAF field and
the NULBAF field. A Format Index is valid if the value is less than the sum of the values represented by the
NLBAF field and the NULBAF field. An LBA Format that is supported, but not currently available is indicated
by clearing the LBA Data Size field to 0h for that LBA Format.

**Figure 175: LBA Format List Structure**

LBA Format 0 Support

LBA Format 1 Support

...

LBA Format NLBAF - 1 Support
Supported format
capabilities the same
Number of LBA Formats
(refer to NLBAF)

LBA Format NLBAF  Support

LBA Format NLBAF+1 Support

...

LBA Format NLBAF+NULBAF-1 Support
Supported format
capabilities unique

Number of Non-Common
LBA Formats
(refer to NULBAF )
152

**Figure 176: LBA Format List Entries Applicability to Identify Command CNS Value**

**CNS**

**Value**

**Returned data is associated with LBA**

**Format entries referenced by only the**

**NLBAF field**

**Returned data is associated with LBA Format**

**entries referenced by both the NLBAF field and**

**NULBAF field**
00h
Yes
No
05h
Yes
No
08h
Yes
No
09h
No
Yes
0Ah
No
Yes

**5.6**

**LBA Migration Queue**

As defined by the NVM Express Base Specification, a User Data Migration Queue allows a controller to
post entries that identify user data modifications due to the processing of commands by the controller
associated to the User Data Migration Queue. For the NVM Command Set:
•
user data is logical blocks and posted entries indicate:
o
data in the logical blocks has changed (e.g., modified by a Write command);
o
data in the logical blocks may have changed (e.g., a Write command was processed that
targeted the logical blocks but there was no change to the data in those logical blocks);
o
are deallocated (i.e., the logical block transitioned from being allocated to deallocated); or
o
may have been deallocated (i.e., the command requested to deallocate logical blocks that
were already deallocated);
and
•
the User Data Migration Queue is referred to as the LBA Migration Queue.
If logging has been started in an LBA Migration Queue due to a Track Send command (refer to the NVM
Express Base Specification), the first entry posted indicates that the logging has started. Subsequent
entries are able to indicate if an entry is:
•
the last entry due to the controller associated with the LBA Migration Queue being suspended as
a result of a Migration Send command (refer to the NVM Express Base Specification);
•
the last entry due to logging being stopped as a result of the controller processing a command that
is defined to stop logging (e.g., the Track Send command (refer to the NVM Express Base
Specification));
•
the controller detecting that the LBA Migration Queue has become full; or
•
the first entry due to the controller associated with the LBA Migration Queue being resumed while
suspended as a result of a Migration Send command.

**LBA Migration Queue Entries**
The LBA Migration Queue Format (LBAMQF) field in the I/O Command Set specific Identify Controller data
structure (refer to Figure 120) defines the supported format for entries in an LBA Migration Queue. Figure
177 defines the supported format.
A controller may aggregate the results of multiple commands processed by a controller into a single entry.
For example:
•
If the controller processes three sequential Write commands, then the controller may post a single
entry that incorporates all of the logical blocks written.
•
If the controller processes the sequential commands that modify the same LBA range, then the
controller may post a single entry for the LBA range with the result from the last command of that
set of sequential commands.


|CNS<br>Value||Returned data is associated with LBA|||Returned data is associated with LBA Format||
|---|---|---|---|---|---|---|
|||Format entries referenced by only the|||entries referenced by both the NLBAF field and||
|||NLBAF field|||NULBAF field||
|00h|Yes|||No|||
|05h|Yes|||No|||
|08h|Yes|||No|||
|09h|No|||Yes|||
|0Ah|No|||Yes|||

153
The controller shall only post an entry into an LBA Migration queue if the processing for the command
reported by the entry has taken effect, which may be before the completion for that command is posted.
For example, if a Write command is processed by a controller that results in the posting of an entry in the
LBA Migration queue that has:
•
LBAINR bit cleared to ‘0’;
•
the SLBA field set to the SLBA field of that Write command; and
•
the NLB field set to the NLB field of that Write command,
then the host may issue a Read command to obtain the logical blocks written even if the completion for that
Write command is not posted.
If:
•
the controller processes a command that is a request to modify a logical block; and
•
that modification results:
o
in the logical block remaining in the same condition (e.g., host deallocates a logical block
that is already deallocated); or
o
the logical block has the exact same data (e.g., the controller processes a Write Zeroes
command for a logical block that already is written with zero data),
then the controller may or may not report that logical block in an entry in the LBA Migration Queue.

**Figure 177: LBA Migration Queue Entry Type 0**

**Bytes**

**Description**

03:00
Namespace Identifier (NSID): This field indicates the namespace identifier associated with the logical
blocks reported in this entry.
If the LBACIR field is set to 10b, then this field shall be cleared to 0h and should be ignored by the host.

07:04
Number of Logical Blocks (NLB): This field indicates the number of logical blocks reported by this entry.
This is a 0’s based value.
If the LBACIR field is set to 10b, then this field shall be cleared to 0h and should be ignored by the host.

15:08
Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block of data reported by
this entry.
If the LBACIR field is non -zero, then this field shall be cleared to 0h and should be ignored by the host.
30:16
Reserved


||Bytes|||Description||
|---|---|---|---|---|---|
|03:00|||Namespace Identifier (NSID): This field indicates the namespace identifier associated with the logical<br>blocks reported in this entry.<br>If the LBACIR field is set to 10b, then this field shall be cleared to 0h and should be ignored by the host.|||
|07:04|||Number of Logical Blocks (NLB): This field indicates the number of logical blocks reported by this entry.<br>This is a 0’s based value.<br>If the LBACIR field is set to 10b, then this field shall be cleared to 0h and should be ignored by the host.|||
|15:08|||Starting LBA (SLBA): This field indicates the 64-bit address of the first logical block of data reported by<br>this entry.<br>If the LBACIR field is non -zero, then this field shall be cleared to 0h and should be ignored by the host.|||
|30:16|||Reserved|||

154

**Figure 177: LBA Migration Queue Entry Type 0**

**Bytes**

**Description**

**LBA Migration Queue Attributes (LBAMQA): This field indicates attributes associates with the LBE**

**Migration Queue entry.**

**Bits**

**Description**

07:06

**LBA Change Information Attribute (LBACIR): This field indicates attributes associated with**
the reporting of the LBA range in this entry.
If the ESA field is cleared to 000b, then this field shall be cleared to 00b.

**Value**

**Definition**
00b
This entry is reporting logical blocks that have changed in the reported namespace.
The SLBA field and the NLB field identify the LBA range.
01b
This entry is reporting that all logical blocks in the reported namespace have
changed.
10b
This value indicates that no LBA range is being reported by this entry.
11b
Reserved

**Deallocated LBAs (DLBA): If this bit is set to ‘1’, then: the logical blocks reported by this entry**
have been deallocated.
If this bit is cleared to ‘0’, then the logical blocks reported by this entry have been modified (e.g.,
been written or deallocated).
Reserved

03:01
Entry Sequence Attribute (ESA): This field specifies the attribute of this entry related to starting
and stopping of the posting of entries into the LBA Migration Queue.

**Value**

**Definition**

000b
This entry is not the:
•
first entry placed into the LBA Migration Queue since:
o
logging was started; or
o
the controller associated with the LBA Migration Queue
resumed from a suspended state;
and
•
last entry placed into the LBA Migration Queue since logging was
stopped or the controller associated with the LBA Migration Queue
was suspended.

001b
This is the first entry placed into the LBA Migration Queue since:
•
logging was started; or
•
the controller associated with the LBA Migration Queue resumed
from a suspended state.
010b
This is the last entry placed into the LBA Migration Queue as a result of
logging being stopped due to a request from the host.
011b
This is the last entry placed into the LBA Migration Queue as a result of the
controller associated with the LBA Migration Queue being suspended.
100b to 110b
Reserved

111b
This is the last entry placed into the LBA Migration Queue due to the LBA
Migration Queue becoming full. This value notifies the host that the controller
has stopped logging logical block changes into that LBA Migration Queue.

**Controller Data Queue Phase Tag (CDQP): This bit identifies whether a LBA Migration Queue**
entry is new as defined by the Controller Data Queue Phase Tag section in the NVM Express
Base Specification.


||Bytes|||Description||
|---|---|---|---|---|---|
|31|||LBA Migration Queue Attributes (LBAMQA): This field indicates attributes associates with the LBE<br>Migration Queue entry.<br>Bits Description<br>LBA Change Information Attribute (LBACIR): This field indicates attributes associated with<br>the reporting of the LBA range in this entry.<br>If the ESA field is cleared to 000b, then this field shall be cleared to 00b.<br>Value Definition<br>07:06 This entry is reporting logical blocks that have changed in the reported namespace.<br>00b<br>The SLBA field and the NLB field identify the LBA range.<br>This entry is reporting that all logical blocks in the reported namespace have<br>01b<br>changed.<br>10b This value indicates that no LBA range is being reported by this entry.<br>11b Reserved<br>Deallocated LBAs (DLBA): If this bit is set to ‘1’, then: the logical blocks reported by this entry<br>have been deallocated.<br>05<br>If this bit is cleared to ‘0’, then the logical blocks reported by this entry have been modified (e.g.,<br>been written or deallocated).<br>04 Reserved<br>Entry Sequence Attribute (ESA): This field specifies the attribute of this entry related to starting<br>and stopping of the posting of entries into the LBA Migration Queue.<br>Value Definition<br>This entry is not the:<br>• first entry placed into the LBA Migration Queue since:<br>o logging was started; or<br>o the controller associated with the LBA Migration Queue<br>000b resumed from a suspended state;<br>and<br>• last entry placed into the LBA Migration Queue since logging was<br>stopped or the controller associated with the LBA Migration Queue<br>03:01<br>was suspended.<br>This is the first entry placed into the LBA Migration Queue since:<br>001b • logging was started; or<br>• the controller associated with the LBA Migration Queue resumed<br>from a suspended state.<br>This is the last entry placed into the LBA Migration Queue as a result of<br>010b<br>logging being stopped due to a request from the host.<br>This is the last entry placed into the LBA Migration Queue as a result of the<br>011b<br>controller associated with the LBA Migration Queue being suspended.<br>100b to 110b Reserved<br>This is the last entry placed into the LBA Migration Queue due to the LBA<br>111b Migration Queue becoming full. This value notifies the host that the controller<br>has stopped logging logical block changes into that LBA Migration Queue.<br>Controller Data Queue Phase Tag (CDQP): This bit identifies whether a LBA Migration Queue<br>00 entry is new as defined by the Controller Data Queue Phase Tag section in the NVM Express<br>Base Specification.|||


||Bits|||Description||
|---|---|---|---|---|---|
|07:06|||LBA Change Information Attribute (LBACIR): This field indicates attributes associated with<br>the reporting of the LBA range in this entry.<br>If the ESA field is cleared to 000b, then this field shall be cleared to 00b.<br>Value Definition<br>This entry is reporting logical blocks that have changed in the reported namespace.<br>00b<br>The SLBA field and the NLB field identify the LBA range.<br>This entry is reporting that all logical blocks in the reported namespace have<br>01b<br>changed.<br>10b This value indicates that no LBA range is being reported by this entry.<br>11b Reserved|||
|05|||Deallocated LBAs (DLBA): If this bit is set to ‘1’, then: the logical blocks reported by this entry<br>have been deallocated.<br>If this bit is cleared to ‘0’, then the logical blocks reported by this entry have been modified (e.g.,<br>been written or deallocated).|||
|04|||Reserved|||
|03:01|||Entry Sequence Attribute (ESA): This field specifies the attribute of this entry related to starting<br>and stopping of the posting of entries into the LBA Migration Queue.<br>Value Definition<br>This entry is not the:<br>• first entry placed into the LBA Migration Queue since:<br>o logging was started; or<br>o the controller associated with the LBA Migration Queue<br>000b resumed from a suspended state;<br>and<br>• last entry placed into the LBA Migration Queue since logging was<br>stopped or the controller associated with the LBA Migration Queue<br>was suspended.<br>This is the first entry placed into the LBA Migration Queue since:<br>001b • logging was started; or<br>• the controller associated with the LBA Migration Queue resumed<br>from a suspended state.<br>This is the last entry placed into the LBA Migration Queue as a result of<br>010b<br>logging being stopped due to a request from the host.<br>This is the last entry placed into the LBA Migration Queue as a result of the<br>011b<br>controller associated with the LBA Migration Queue being suspended.<br>100b to 110b Reserved<br>This is the last entry placed into the LBA Migration Queue due to the LBA<br>111b Migration Queue becoming full. This value notifies the host that the controller<br>has stopped logging logical block changes into that LBA Migration Queue.|||
|00|||Controller Data Queue Phase Tag (CDQP): This bit identifies whether a LBA Migration Queue<br>entry is new as defined by the Controller Data Queue Phase Tag section in the NVM Express<br>Base Specification.|||


||Value|||Definition||
|---|---|---|---|---|---|
|00b|||This entry is reporting logical blocks that have changed in the reported namespace.<br>The SLBA field and the NLB field identify the LBA range.|||
|01b|||This entry is reporting that all logical blocks in the reported namespace have<br>changed.|||
|10b|||This value indicates that no LBA range is being reported by this entry.|||
|11b|||Reserved|||


||Value|||Definition||
|---|---|---|---|---|---|
|000b|||This entry is not the:<br>• first entry placed into the LBA Migration Queue since:<br>o logging was started; or<br>o the controller associated with the LBA Migration Queue<br>resumed from a suspended state;<br>and<br>• last entry placed into the LBA Migration Queue since logging was<br>stopped or the controller associated with the LBA Migration Queue<br>was suspended.|||
|001b|||This is the first entry placed into the LBA Migration Queue since:<br>• logging was started; or<br>• the controller associated with the LBA Migration Queue resumed<br>from a suspended state.|||
|010b|||This is the last entry placed into the LBA Migration Queue as a result of<br>logging being stopped due to a request from the host.|||
|011b|||This is the last entry placed into the LBA Migration Queue as a result of the<br>controller associated with the LBA Migration Queue being suspended.|||
|100b to 110b|||Reserved|||
|111b|||This is the last entry placed into the LBA Migration Queue due to the LBA<br>Migration Queue becoming full. This value notifies the host that the controller<br>has stopped logging logical block changes into that LBA Migration Queue.|||

155

**5.7**

**Namespace Management**

Namespace Management capability operates as defined in the NVM Express Base Specification with
additional capabilities specifically for the NVM Command Set.
The NVM Command Set supports reporting of Namespace Granularity as I/O Command Set specific
Namespace Management capability content. The Namespace Granularity List defined in Figure 123 is
requested by the host using the Identify command with CNS set to 16h.
If the controller supports reporting of Namespace Granularity, then the Namespace Granularity Descriptor
List (refer to Figure 123) contains one or more Namespace Granularity Descriptors (refer to Figure 124)
indicating the size granularity and the capacity granularity with which the controller creates namespaces.
The size granularity and the capacity granularity are hints which may be used by the host to minimize the
capacity that is allocated for a namespace and that is not able to be addressed by logical block addresses.
The granularities are used in specifying values for the Namespace Size (NSZE) field and Namespace
Capacity (NCAP) field of the data structure used for the create operation of the Namespace Management
command (refer to Figure 124).
If a Namespace Management command create operation specifies values such that:
a) the product of NSZE and the logical block size is an integral multiple of the Namespace Size
Granularity;
b) the product of NCAP and the logical block size is an integral multiple of the Namespace Capacity
Granularity; and
c) NSZE is equal to NCAP,
then the namespace is fully provisioned and all of the capacity allocated for the namespace is able to be
addressed by logical block addresses, otherwise:
a) not all of the capacity allocated for the namespace is able to be addressed by logical block
addresses; and
b) if the Namespace Management command is otherwise valid, then the controller shall not abort the
command (i.e., the granularity values are hints).

**5.8**

**NVM Command Set Media and Data Error Handling**

Media and Data Error handling operates as described in the NVM Express Base Specification with the
following extensions.
If a write error occurs during the processing of a command, (e.g., an internal error, End-to-end Guard Check
Error, End-to-end Application Tag Check Error), the controller may either stop or complete the DMA
transfer. If the write size is less than or equal to the Atomic Write Unit Power Fail size, then subsequent
reads for the associated logical blocks shall return data from the previous successful write operation. If the
write size is larger than the Atomic Write Unit Power Fail size, then subsequent reads for the associated
logical blocks may return data from the previous successful write operation or this failed write operation.
Based on the value of the Limited Retry bit, the controller may apply all available error recovery means to
complete the command.

**5.9**

**Reservations**

Reservations operate as defined in the NVM Express Base Specification with the additional I/O Command
Set specific Command Behavior in the Presence of a Reservation defined in Figure 178.
156

**Figure 178: Command Behavior in the Presence of a Reservation**

**NVMe Command**

**Write**

**Exclusive**

**Reservation**

**Exclusive**

**Access**

**Reservation**

**Write Exclusive**

**Registrants Only**

**or**

**Write Exclusive**

**All Registrants**

**Reservation**

**Exclusive Access**

**Registrants Only**

**or**

**Exclusive Access**

**All Registrants**

**Reservation**

**Non-Registrant**

**Registrant**

**Non-Registrant**

**Registrant**

**Non-Registrant**

**Registrant**

**Non-Registrant**

**Registrant**

**Read Command Group**
Compare
Copy (source)1
Read
Verify
A
A
C
C
A
A
C
A

**Write Command Group**
Copy (destination)1
Dataset Management
Write
Write Uncorrectable
Write Zeroes
C
C
C
C
C
A
C
A

Key:
A definition: A=Allowed, command processed normally by the controller
C definition: C=Conflict, command aborted by the controller with status Reservation Conflict

Notes:
1.
Each source namespace of a Copy command is checked for reservation conflict as if accessed by a read command
and the destination namespace of a Copy command is checked for reservation conflict as if accessed by a write
command.


**5.10 Sanitize Operations**

Sanitize operates as defined in the NVM Express Base Specification. NVM Command Set specific
definitions and extensions are defined in this section.
Following a successful sanitize operation, the values of user data (including protection information, and
non-PI metadata) that result from an audit (refer to the NVM Express Base Specification) of the sanitization
target are specified in Figure 179.
If the controller does not deallocate logical blocks as part of processing a sanitize operation, then following
a successful completion of that sanitize operation:
•
if the controller processes a read command specifying protection information checking (i.e., the
PRCHK field is set to a non-zero value or the STC bit is set to ‘1’) before a write operation is
performed on the logical blocks specified by that read command, then the controller may abort that
read command with a status code indicating a protection information check error (refer to the Media
and Data Integrity Errors Definition section of the NVM Express Base Specification).
If the controller deallocates logical blocks as part of processing a sanitize operation, then after successful
completion of that sanitize operation, the values read from deallocated logical blocks are described in


|NVMe Command||Write<br>Exclusive<br>Reservation||||||Exclusive<br>Access<br>Reservation||||||Write Exclusive<br>Registrants Only<br>or<br>Write Exclusive<br>All Registrants<br>Reservation||||||Exclusive Access<br>Registrants Only<br>or<br>Exclusive Access<br>All Registrants<br>Reservation|||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||Non-Registrant|||Registrant|||Non-Registrant|||Registrant|||Non-Registrant|||Registrant|||Non-Registrant|||Registrant|||
||Read Command Group||||||||||||||||||||||||||
|Compare<br>1<br>Copy (source)<br>Read<br>Verify||A|||A|||C|||C|||A|||A|||C|||A||||
||Write Command Group||||||||||||||||||||||||||
|1<br>Copy (destination)<br>Dataset Management<br>Write<br>Write Uncorrectable<br>Write Zeroes||C|||C|||C|||C|||C|||A|||C|||A||||
|Key:<br>A definition: A=Allowed, command processed normally by the controller<br>C definition: C=Conflict, command aborted by the controller with status Reservation Conflict<br>Notes:<br>1. Each source namespace of a Copy command is checked for reservation conflict as if accessed by a read command<br>and the destination namespace of a Copy command is checked for reservation conflict as if accessed by a write<br>command.|||||||||||||||||||||||||||

157
section 3.3.3.2.1. The host may specify that sanitized logical blocks not be deallocated by setting the No-
Deallocate After Sanitize bit to ‘1’ in the Sanitize command.

**Figure 179: Sanitize Operation Types – User Data Values**

**Sanitize Operation**

**Type**

**User Data**
Block Erase
Vendor specific value
Crypto Erase
Indeterminate value
Overwrite
Refer to Sanitize Operations – Overwrite Mechanism in the NVM Express Base
Specification

**Media Verification**
While the sanitization target is in the Media Verification state (refer to the Sanitize Operation State Machine
Section in the NVM Express Base Specification), the controller processes Read commands as described
in this section and shall not abort those commands with a status code of Sanitize In Progress or Sanitize
Namespace In Progress.
If:
•
the controller processes a Read command that does not specify any Protection Information (PI)
checking (i.e., the PRCHK field is cleared to 000b (refer to Figure 11) and the STC bit is cleared to
‘0’ (refer to Figure 12));
•
each LBA specified by that Read command is in a sanitization target that is in the Media Verification
state (i.e., is in the NVM subsystem for a sanitization target of the NVM subsystem or is in the
namespace for a sanitization target of a namespace); and
•
for each LBA specified by that command for which media is allocated, the controller is able to read
data from the media,
then:
•
for each LBA specified by that command for which media is allocated, the controller:
o
shall ignore data integrity errors, if any (e.g., shall not abort that command with a status
code of Unrecovered Read Error if the controller is able to read that media);
o
shall return data that is read from that media; and
o
may return different data for successive reads (i.e., without any writes between those
reads) of the same LBA (e.g., to obscure media reliability);
•
for each LBA specified by that command for which media is not allocated, the controller shall return
data or abort that command with a status code of Deallocated or Unwritten Logical Block as
described in section 3.3.3.2.1; and
•
the controller shall complete that command with a status code of Successful Media Verification
Read if the command has not been aborted with a different status code (e.g., Deallocated or
Unwritten Logical Block).
If the controller processes a Read command that does not specify any PI checking and is unable to read
the data from the media for any LBA specified by that command for which media is allocated, then the
controller shall abort the command with a status code of Unrecovered Read Error.
If the controller processes a Read command specifying PI checking (i.e., the PRCHK field is set to a non-
zero value or the STC bit is set to ‘1’), then the controller shall abort that command with a status code of
Invalid Field in Command.


||Sanitize Operation||User Data|
|---|---|---|---|
||Type|||
|Block Erase|||Vendor specific value|
|Crypto Erase|||Indeterminate value|
|Overwrite|||Refer to Sanitize Operations – Overwrite Mechanism in the NVM Express Base<br>Specification|

158


**5.11 Streams**

Streams operate as defined in the NVM Express Base Specification. The unit of granularity for the NVM
Command Set specific definition of the Stream Write Size (SWS) field is in logical blocks.
