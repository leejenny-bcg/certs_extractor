# LLM Classifications (Stage 4.5)

568 candidates evaluated. confidence="high" or "medium" generic_administrative/fragment_or_criterion results are applied as flags (hidden by the UI's "hide low-quality entries" checkbox) -- everything else (low confidence, or "benefit") is left alone, per the precision gate.

## "$130 allowance for frames or elective contact lenses" -> benefit (confidence=medium)
- The name describes a specific, nameable vision benefit -- a $130 allowance toward frames or elective contact lenses -- which a member could point to and ask about. It names a concrete covered item/allowance rather than a generic category or a condition/exclusion. Confidence is medium because it's phrased partly as an allowance amount, but it clearly refers to a specific vision benefit.

## "$150 allowance for frames" -> fragment_or_criterion (confidence=medium)
- This is a benefit limitation/allowance amount describing the dollar coverage for frames, not itself a nameable service. The actual benefit is 'frames'; '$150 allowance for frames' describes the allowance/limit terms, appearing under a 'Frequency' section listing coverage parameters. It's a qualifier on how frames are covered rather than a distinct service.

## "$150 allowance for frames or elective contact lenses" -> benefit (confidence=medium)
- This names a specific vision benefit - an allowance amount toward frames or elective contact lenses. A member could point to this and ask about coverage. While phrased with a dollar amount, it refers to a concrete, nameable covered item/allowance rather than a generic category or a mere criterion.

## "$150 elective contact lenses" -> benefit (confidence=medium)
- This names a specific vision benefit -- elective contact lenses with a $150 allowance. Despite the dollar amount prefix (likely an extraction artifact), the core refers to a real, nameable covered item (elective contact lenses).

## "$50 per day for lodging" -> fragment_or_criterion (confidence=high)
- This is a cost/allowance amount ('$50 per day for lodging'), describing a daily reimbursement limit within oncology clinical trials, not a nameable specific service. It's a benefit parameter/limitation, not a service a member would point to and ask if covered.

## "$60 per day for travel" -> fragment_or_criterion (confidence=high)
- This is a dollar allowance amount ('$60 per day for travel'), not a nameable service. It describes a cost/reimbursement limit within the oncology clinical trials provision, not a specific covered service a member could point to and ask about.

## "A DME supplier" -> fragment_or_criterion (confidence=high)
- 'A DME supplier' names a type of provider/source from which equipment may be obtained, not a specific covered service or item. It appears as a list item describing where to obtain equipment, making it a fragment/criterion rather than a nameable benefit.

## "A certified registered nurse anesthetist (CRNA)" -> benefit (confidence=medium)
- The name refers to a certified registered nurse anesthetist, a specific type of provider whose services (anesthesia) are a nameable, specific covered service under Anesthesiology Services. A member could reasonably ask if CRNA services are covered. While it names a provider type rather than a procedure, it points to a specific, identifiable service, so I lean toward benefit.

## "A change in the patient's condition" -> fragment_or_criterion (confidence=high)
- The name 'A change in the patient's condition' does not name any specific service or item. It describes a scenario or condition (likely a criterion for replacing a prosthetic/orthotic device), not a nameable benefit.

## "A licensed behavior analyst (LBA)" -> fragment_or_criterion (confidence=medium)
- This names a type of provider (a licensed behavior analyst), not a specific covered service or item. It describes who renders care rather than a nameable benefit a member would ask about being covered. Under Autism Spectrum Disorders, this is likely a provider-qualification/eligibility reference rather than a benefit name.

## "A licensed psychologist" -> fragment_or_criterion (confidence=high)
- 'A licensed psychologist' names a type of provider, not a specific covered service or item. It appears as part of eligibility criteria describing who may provide autism-related services, not as a nameable benefit a member would ask to have covered.

## "A medical evaluation at an affiliated immunization pharmacy" -> benefit (confidence=medium)
- This names a specific, identifiable service -- a medical evaluation performed at an affiliated immunization pharmacy -- that a member could point to and ask if it's covered. It appears in a list alongside other clear benefits like pre-surgical consultations and ABA treatments. While it includes a location qualifier, the core is a nameable service.

## "A member’s home" -> fragment_or_criterion (confidence=medium)
- 'A member's home' is not a specific covered service or item; it describes a location/setting (likely part of a phrase like 'delivery in a member's home'). It names no nameable service on its own, so it reads as a fragment rather than a benefit.

## "A participating hospice inpatient unit" -> fragment_or_criterion (confidence=medium)
- The name 'A participating hospice inpatient unit' is a sub-item describing WHERE inpatient care is provided (the facility/provider type), not a nameable service itself. The actual benefit is 'Inpatient care provided by...' and this is a list continuation describing the qualifying provider. It reads as a descriptive fragment/provider qualifier rather than a distinct covered service.

## "A participating hospital (when you are discharged)" -> fragment_or_criterion (confidence=high)
- The name is a parenthetical scenario/condition ('when you are discharged') attached to a location, not a specific nameable service or item. It describes a circumstance rather than a covered benefit.

## "A participating hospital contracting with the hospice program or" -> fragment_or_criterion (confidence=high)
- This is a sentence fragment describing a type of provider setting where inpatient hospice care may be delivered, ending in 'or' as part of a list. It does not name a specific covered service; it's a fragment describing a facility qualifier.

## "A participating hospital setting" -> fragment_or_criterion (confidence=high)
- This describes a location/setting where a service (vaginal delivery or cesarean section) is provided, not a specific nameable service itself. It's a qualifier/condition describing where the actual benefit occurs, not a benefit name.

## "A participating skilled nursing facility contracting with the hospice program" -> fragment_or_criterion (confidence=high)
- This describes a type of facility/setting where hospice care is provided, not a specific nameable service. It's a fragment describing a location/provider condition within the hospice benefit, not itself a benefit a member could point to and ask if it's covered.

## "A physical therapy, occupational therapy or speech language therapy visit" -> fragment_or_criterion (confidence=medium)
- The name is phrased as 'A physical therapy, occupational therapy or speech language therapy visit' -- worded as a countable instance/scenario rather than a clean service name. While it references real therapy services, the phrasing ('A ... visit') suggests it was extracted from a cost-share or visit-limit context describing a scenario/unit rather than naming a distinct benefit. The underlying services (PT/OT/speech therapy) are real benefits, but this specific extracted string reads as a fragment describing a visit type. Given real doubt, medium confidence.

## "A physician other than the operating physician" -> fragment_or_criterion (confidence=high)
- This describes who anesthesia services are payable to (a qualifying provider condition), not a specific nameable service. The actual benefit is anesthesia services; this phrase is a criterion/qualifier about the provider, not a service itself.

## "A physician who orders and supervises anesthesiology services" -> fragment_or_criterion (confidence=medium)
- This describes a type of provider/scenario ('a physician who orders and supervises anesthesiology services') rather than naming a specific service. It appears in a list of who may perform anesthesia services, functioning as a qualifier/provider description rather than a nameable benefit a member would ask 'is this covered?'

## "A pre-surgical consultation" -> benefit (confidence=medium)
- 'A pre-surgical consultation' names a specific, identifiable medical service that a member could ask whether it's covered. Despite the article 'A' making it read like a fragment, it refers to a concrete nameable service rather than a category, process word, or eligibility condition. Leaning toward benefit per guidance.

## "A pre-surgical consultation with a specialist" -> benefit (confidence=medium)
- The name refers to a specific, nameable service -- a pre-surgical consultation with a specialist -- which a member could point to and ask about coverage. It appears under copayment/in-network provider headers, but the name itself denotes a concrete service rather than a generic category or a fragment/criterion.

## "A primary care physician office, home, virtual or outpatient visit" -> benefit (confidence=medium)
- The name refers to a specific, nameable service -- a primary care physician visit across various settings (office, home, virtual, outpatient). A member could point to this and ask if it's covered. While phrased somewhat descriptively, it names a concrete service rather than a generic category or a pure eligibility criterion.

## "A private room or an apartment" -> fragment_or_criterion (confidence=medium)
- 'A private room or an apartment' is not a specific nameable medical service or item a member would ask coverage about. It appears in an exclusion list describing accommodation scenarios/conditions rather than naming a distinct benefit. It reads as a fragment describing a room type/scenario, not a service. Not driven by exclusion status but by the name itself lacking a nameable service.

## "A retail health clinic visit" -> benefit (confidence=high)
- A retail health clinic visit names a specific, identifiable service a member could ask about, listed alongside other specific visit types. It refers to a concrete, nameable service rather than a generic category or a fragment/criterion.

## "A single and a tandem transplant" -> benefit (confidence=medium)
- This names a specific transplant configuration (a single transplant combined with a tandem transplant) within Transplant Services. It refers to a concrete, nameable service arrangement a member could ask about, parallel to 'Two tandem transplants' and 'Allogeneic Transplants'. While phrased somewhat as a scenario, it identifies a specific covered transplant scenario rather than a generic category or pure eligibility rule.

## "A specialist office, home, virtual or outpatient visit" -> fragment_or_criterion (confidence=low)
- The name describes a visit setting/scenario ('a specialist office, home, virtual or outpatient visit') phrased as a descriptive clause under Copayment Requirements rather than naming a discrete, nameable service. However, it does reference a specialist visit which could be seen as a service, so confidence is low; it reads more like a cost-share applicability descriptor than a specific benefit.
- **Not auto-flagged**: below the high/medium-confidence precision gate.

## "A speech language pathologist certified by the American Speech-Language-Hearing" -> fragment_or_criterion (confidence=high)
- The name is a truncated sentence fragment describing who must perform the service ('A speech language pathologist certified by the American Speech-Language-Hearing...') rather than naming a specific covered service. It reads as a provider-qualification/eligibility criterion, not a benefit itself. The actual benefit would be 'Speech Language Therapy' (the header).

## "A virtual primary care visit" -> benefit (confidence=high)
- 'A virtual primary care visit' names a specific, nameable service a member could ask about coverage for. It appears in a list of covered visit types alongside office visits and retail clinic visits. This is a real benefit, not a category word or fragment.

## "Act of War" -> fragment_or_criterion (confidence=high)
- 'Act of War' is not a specific nameable service or item. The excerpt shows it as part of an exclusion condition -- services resulting from injury 'due to an act of war.' It describes a scenario/circumstance, not a covered service.

## "Acute Care" -> benefit (confidence=medium)
- Acute care is a defined term referring to a specific level/type of medical care ('Medical care that requires a wide range of medical, surgical, obstetrical...'). It names a recognizable, nameable type of care a member could ask about, appearing alongside real services like Custodial care. It leans more toward a nameable service than a pure administrative category word.

## "Acute renal (kidney) failure" -> benefit (confidence=medium)
- Acute renal (kidney) failure is a specific, nameable medical condition appearing under Dialysis Services, likely as a covered diagnosis/scenario for dialysis. While it's a condition rather than a service per se, it names a specific medical entity a member could point to, and the instructions favor leaning toward benefit when uncertain.

## "Additional Counseling and Screening Services, including but not limited to:" -> fragment_or_criterion (confidence=medium)
- The name ends with 'including but not limited to:' which is an introductory lead-in phrase to a list, not a specific nameable service. 'Additional Counseling and Screening Services' is a vague category rather than a specific benefit, and the trailing colon confirms it's a header/fragment introducing subsequent items rather than a benefit name itself.

## "Adjunctive G eneral Services" -> generic_administrative (confidence=medium)
- 'Adjunctive General Services' is a category heading in dental plans (a section grouping in CDT coding) rather than a specific nameable service. It describes a class of miscellaneous services rather than a single item a member could point to. No snippet available, but the name and Class II Basic Services header suggest a category grouping.

## "Adjunctive general services" -> generic_administrative (confidence=medium)
- 'Adjunctive general services' is a category/grouping heading that introduces a list of specific services ('These services include: ...'), rather than naming one specific, nameable service itself. It functions as a category label within Class II Basic Services, similar to 'Other Services'.

## "Adjustments" -> benefit (confidence=medium)
- The name 'Adjustments' refers to a specific dental service (adjustments/relines/repairs for prosthodontic appliances, or occlusal adjustments) that a member could ask about. While the word is somewhat generic on its own, in the dental context it names an identifiable procedure. Leaning toward benefit given the specific service context.

## "Adjustments, repairs, relines, rebases and tissue conditioning for prosthodontic appliances" -> benefit (confidence=high)
- The name refers to specific, nameable dental services (adjustments, repairs, relines, rebases, tissue conditioning for prosthodontic appliances) under Class II Basic Services. These are concrete procedures a member could ask about coverage for.

## "Administration of blood" -> benefit (confidence=high)
- 'Administration of blood' names a specific, nameable medical service (blood transfusion administration) appearing under the Surgery benefits section. A member could ask whether this is covered.

## "Administration of covered drugs except for select immunization vaccines" -> fragment_or_criterion (confidence=medium)
- The name 'Administration of covered drugs except for select immunization vaccines' contains an exception clause qualifier and describes a process/scenario rather than a specific nameable service. It appears in an exclusion list alongside other fragment-style items like 'Anything other than covered drugs and services' and 'Any covered drug entirely consumed at the time and place of the prescription.' While 'administration of drugs' could be a service, the 'except for select immunization vaccines' qualifier makes this read as a carved-out condition rather than a clean benefit name.

## "Air Ambulance" -> benefit (confidence=high)
- Air ambulance is a specific, nameable transport service a member could ask about coverage for, appearing under Ambulance Services.

## "Allergy Testing" -> benefit (confidence=high)
- Allergy testing is a specific, nameable medical service that a member could point to and ask if it's covered. It appears consistently under a clinical service header.

## "Allergy Therapy" -> benefit (confidence=high)
- Allergy Therapy names a specific, identifiable medical service (allergy immunotherapy, allergy shots, injections). A member could ask whether it is covered. It is not a generic administrative category or a fragment.

## "Allergy immunotherapy by injection (allergy shots)" -> benefit (confidence=high)
- The name refers to a specific, nameable medical service -- allergy immunotherapy administered by injection (allergy shots). It's a concrete service a member could ask about, and appears under a clinically relevant header.

## "Allogeneic" -> benefit (confidence=medium)
- The name 'Allogeneic' is an adjective typically qualifying 'Transplants', and the excerpts show 'Allogeneic Transplants' as a specific, nameable transplant service. Allogeneic transplants are a real, specific covered service (donor-derived stem cell/bone marrow transplants). The truncation to just 'Allogeneic' is an extraction artifact, but it clearly refers to a specific nameable service.

## "Allogeneic Oncology Clinical Trials" -> benefit (confidence=medium)
- The name refers to a specific type of oncology clinical trial (allogeneic - involving donor cells/tissue), which is a nameable service a member could ask about coverage for. It names a specific category of covered service rather than a generic administrative process or a fragment. No excerpts available, but the name itself is specific enough to be a benefit.

## "Allogeneic Transplants" -> benefit (confidence=high)
- Allogeneic Transplants names a specific, recognizable medical procedure (transplant using donor cells/tissue). It is a nameable service a member could ask about, appearing under Transplant Services as a distinct benefit.

## "Alveoloplasty" -> benefit (confidence=high)
- Alveoloplasty is a specific, nameable dental surgical procedure (surgical reshaping of the alveolar bone/jaw ridge). It appears in a list of payable procedures alongside other specific dental services, and a member could clearly ask 'is this covered?'

## "Alveoloplasty needed to prepare for a denture" -> benefit (confidence=high)
- Alveoloplasty is a specific, nameable dental surgical procedure (reshaping of the alveolar bone). The qualifier 'needed to prepare for a denture' describes the clinical context but the core names a real service a member could ask about. It appears in a list of specific procedures under Class III Major Services.

## "Alveoplasty" -> benefit (confidence=high)
- Alveoplasty is a specific, nameable surgical dental procedure (surgical reshaping of the alveolar ridge). A member could point to it and ask if it's covered. It's a real service, not a generic category or fragment.

## "Amalgam Fillings" -> benefit (confidence=high)
- Amalgam fillings are a specific, nameable dental service that a member could ask about being covered. This is a concrete restorative service, not a generic category or fragment.

## "An office consultation" -> benefit (confidence=high)
- An office consultation is a specific, nameable medical service that a member could ask about being covered. It appears in a list alongside other specific services like pre-surgical consultation and ABA treatment. The leading article does not make it generic; it names a concrete service.

## "An office consultation with a specialist" -> benefit (confidence=high)
- This names a specific, identifiable service -- an office consultation with a specialist -- that a member could ask about coverage for. It appears alongside other specific visit types with defined copayments. It is not a generic category word or a fragment/criterion.

## "Ancillary services" -> generic_administrative (confidence=medium)
- "Ancillary services" is a broad category noun referring to a general class of supporting services rather than a specific, nameable covered service. It appears in a list alongside 'Services provided by staff' and 'Prescribed drugs,' functioning as a category rather than a distinct point-and-ask benefit.

## "Anesthesia during infusion therapy" -> benefit (confidence=high)
- 'Anesthesia during infusion therapy' names a specific, nameable service (local anesthesia provided as part of infusion therapy). It appears as a distinct bulleted benefit under Anesthesiology Services, and a member could clearly ask whether this is covered.

## "Anesthesia services and materials" -> benefit (confidence=high)
- Anesthesia services and materials is a specific, nameable medical service that a member could ask about being covered. It appears in a bulleted list of covered surgery-related services alongside other concrete benefits like recovery room and nursing care.

## "Anesthesiology during surgery" -> benefit (confidence=high)
- 'Anesthesiology during surgery' names a specific, nameable medical service - anesthesia given to members undergoing covered surgery. A member could point to it and ask if it's covered. It appears under 'We pay for' with concrete descriptions of the service.

## "Anti reflective coating" -> benefit (confidence=high)
- Anti reflective coating is a specific, nameable lens option that a member could ask whether it is covered. It appears in a bulleted list of concrete lens options under the Lenses section, alongside similar specific items like polycarbonate lenses and progressive lenses.

## "Antibiotic injections" -> benefit (confidence=high)
- 'Antibiotic injections' names a specific, identifiable dental service listed under Class II Basic Services. A member could point to it and ask if it's covered. It is not a generic category word nor a fragment/criterion.

## "Antireflective Lenses" -> benefit (confidence=high)
- Antireflective lenses is a specific, nameable vision item that a member could point to and ask if it's covered. The fact that it appears in an exclusion/member-responsibility list does not change its status as a real benefit item.

## "Any drug we think is experimental or investigational." -> fragment_or_criterion (confidence=high)
- The name describes a category/condition ('any drug we think is experimental or investigational') rather than naming a specific, pointable service or item. It is a qualifier/exclusion criterion appearing in a list of excluded drug types, describing the scenario under which drugs are not covered rather than naming a discrete service.

## "Any medically necessary special features" -> fragment_or_criterion (confidence=medium)
- 'Any medically necessary special features' does not name a specific service or item; it describes a qualifier/scenario (additional features that meet a medical necessity criterion) rather than a nameable prosthetic/orthotic device or service. It reads as a condition-based catch-all within the device coverage list.

## "Any procedure done to enhance reproductive capacity or fertility" -> fragment_or_criterion (confidence=high)
- The phrase 'Any procedure done to enhance reproductive capacity or fertility' describes a category/scenario of procedures via a qualifying description rather than naming a specific, nameable service. It begins with 'Any procedure done to...' which is a descriptive criterion, not a distinct service a member could point to and ask about specifically.

## "Anything other than covered drugs and services" -> fragment_or_criterion (confidence=high)
- The phrase 'Anything other than covered drugs and services' names no specific service or item; it is a catch-all exclusion scenario describing a category of non-covered things, not a nameable benefit.

## "Aphakic" -> benefit (confidence=high)
- Appears in a list of special lens types (Myodisc, Lenticular myodisc, Aphakic, etc.). 'Aphakic' names a specific type of lens for aphakic (post-cataract) patients -- a concrete, nameable item a member could ask about, regardless of its exclusion status here.

## "Apical surgeries on permanent teeth" -> benefit (confidence=high)
- 'Apical surgeries on permanent teeth' names a specific, nameable dental procedure (apicoectomy/apical surgery), listed as a specific service under endodontic services. A member could point to it and ask if it's covered.

## "Applied Behavior Analysis (ABA) treatment" -> benefit (confidence=high)
- ABA is a specific, nameable therapeutic service for autism spectrum disorders that a member could ask whether it's covered. It appears under an Autism Spectrum Disorders benefit section, confirming it's a real benefit.

## "Approved clinical trial" -> benefit (confidence=medium)
- 'Approved clinical trial' names a specific, nameable item/service (a defined phase I-IV clinical trial for prevention/detection/treatment) that a member could point to and ask about coverage of routine patient costs. It refers to a concrete covered scenario rather than a generic category word or a mere condition/qualifier. Medium confidence since it functions partly as a defined term, but it clearly names a specific coverable service context.

## "Artificial insemination" -> benefit (confidence=high)
- Artificial insemination is a specific, nameable medical procedure listed among infertility treatment services. A member could clearly ask whether it's covered, making it a genuine benefit.

## "Assessments" -> generic_administrative (confidence=medium)
- 'Assessments' is a generic category noun describing a kind of diagnostic activity rather than a specific nameable service. It appears as a bullet under 'Diagnostic services' alongside 'Evaluations or tests,' indicating it's a broad category label rather than a distinct benefit a member could point to. Unlike a specific named test (e.g., Autism Diagnostic Observation Schedule), 'Assessments' alone is too generic.

## "Athletic Trainer" -> fragment_or_criterion (confidence=medium)
- 'Athletic Trainer' names a type of health care provider/professional, not a specific covered service or item. It appears in lists of provider types and a definition of the professional. A provider category is neither a nameable service benefit nor an administrative cost-share term; it functions as a criterion/qualifier for who renders care rather than a benefit itself.

## "Autism Benefit Maximums" -> generic_administrative (confidence=medium)
- The name 'Autism Benefit Maximums' refers to a dollar/visit limit cap on autism coverage, not a specific covered service. It describes a benefit maximum (a cost/limit administrative concept) rather than a nameable service a member could ask 'is this covered?' about.

## "Autism Coverage Requirements" -> fragment_or_criterion (confidence=medium)
- The name 'Autism Coverage Requirements' does not name a specific service or item; it describes the rules/conditions for coverage of autism services rather than a nameable benefit. 'Requirements' signals eligibility criteria rather than a service a member could point to. While the underlying topic (autism spectrum disorder treatment) is a real benefit, this particular name refers to the requirements/criteria, not the service itself.

## "Autism Covered Services" -> generic_administrative (confidence=low)
- The name 'Autism Covered Services' reads as a category/grouping heading for a set of services related to autism rather than a single specific, nameable service. However, without direct excerpts and given it references a real clinical domain, there is genuine doubt, so confidence is low.
- **Not auto-flagged**: below the high/medium-confidence precision gate.

## "Autism Limitations and Exclusions" -> generic_administrative (confidence=medium)
- The name 'Autism Limitations and Exclusions' describes a category/subsection heading listing restrictions rather than naming a specific covered service or item. It's a structural/administrative label for a set of limitations, not a nameable benefit a member could point to and ask if it's covered.

## "Autism Spectrum Disorders - Benefit Maximums" -> generic_administrative (confidence=medium)
- The name refers to 'Benefit Maximums' for Autism Spectrum Disorders, which describes a coverage limit/administrative provision rather than a specific nameable service. While ASD treatment itself is a benefit, this candidate specifically names the maximums category, which is an administrative/limitation concept, not a service a member would point to and ask 'is this covered?'

## "Autism Spectrum Disorders- Covered Services" -> benefit (confidence=medium)
- The name refers to Autism Spectrum Disorders, a specific, nameable condition whose diagnosis and treatment is a real covered service a member could ask about. The '- Covered Services' suffix is a header artifact, but the core is a legitimate benefit. Leaning toward benefit per guidance.

## "Autologous" -> benefit (confidence=medium)
- The candidate 'Autologous' is truncated from 'Autologous Transplants', which refers to a specific, nameable medical procedure (a type of bone marrow transplant using the patient's own cells). Under the 'Transplant Services' / 'Bone Marrow Transplants' header, this names a real covered service. Confidence is medium because the extracted name is a fragment of the full benefit name, but it clearly points to a specific service rather than a generic category or eligibility criterion.

## "Autologous Oncology Clinical Trials" -> benefit (confidence=low)
- The name refers to autologous oncology clinical trials, which appears to name a specific type of service/participation (autologous treatments within oncology clinical trials). Though phrasing is somewhat category-like, it identifies a specific nameable service a member could ask about. No excerpts provided, so confidence is low, but leaning toward benefit per guidance.

## "Autologous Transplants" -> benefit (confidence=high)
- Autologous Transplants is a specific, nameable medical procedure appearing under Transplant Services. A member could point to it and ask if it's covered. It names a real service, not a generic category or fragment.

## "BCBSM-designated providers in Michigan" -> fragment_or_criterion (confidence=medium)
- The name 'BCBSM-designated providers in Michigan' does not name a specific covered service or item; it describes a category of providers/a qualifier about who provides services, appearing under a 'Value Based Programs' header. It reads as a provider designation criterion rather than a nameable benefit a member could ask coverage about.

## "Bariatric surgery" -> benefit (confidence=high)
- Bariatric surgery is a specific, nameable surgical procedure that a member could ask about coverage for. It appears under Surgery section headers and is clearly a distinct covered service, not a generic category or fragment.

## "Bariatric surgery is limited to one per member per lifetime" -> fragment_or_criterion (confidence=high)
- This text states a limitation ('is limited to one per member per lifetime') rather than naming a service. The actual benefit is 'Bariatric surgery' which appears separately; this candidate is a limitation clause describing a frequency criterion, not a nameable service.

## "Basic prosthodontic services" -> benefit (confidence=high)
- 'Basic prosthodontic services' names a specific, recognizable category of dental services (replacing missing natural teeth, adjustments, repairs). It's a concrete, nameable service a member could ask about, appearing under Class II Basic Services. Though somewhat category-like, prosthodontic services is a specific dental service type, not a generic administrative process word.

## "Behavioral health services" -> benefit (confidence=medium)
- 'Behavioral health services' appears as a nameable service category (mental health and substance use disorder services), listed as a covered service. While somewhat broad, it refers to a specific, recognizable set of services a member could ask about. Leaning toward benefit given the guidance to avoid mislabeling legitimate services.

## "Benefit Maximums" -> generic_administrative (confidence=high)
- "Benefit Maximums" is a category/administrative term referring to coverage limits, not a specific nameable service a member could ask to have covered.

## "Bereavement counseling for the family after the member’s death" -> benefit (confidence=high)
- Bereavement counseling is a specific, nameable service provided under hospice care. The qualifier 'for the family after the member's death' describes the specific covered service, and it appears consistently as a hospice benefit component. A member could point to this and ask whether it is covered.

## "Bi-weekly (three-month supply)" -> benefit (confidence=medium)
- Under the 'Contact Lenses' vision header, 'Bi-weekly (three-month supply)' names a specific type/quantity of contact lens supply, which is a nameable covered item a member could ask about. It is not a generic category word or a mere eligibility criterion; it describes a specific lens supply option. Confidence is medium given no excerpt was found, but the name and header point to a real vision benefit.

## "Binocular measure" -> benefit (confidence=high)
- Binocular measure is a specific, nameable diagnostic component of an eye exam (measuring how the eyes work together). It appears alongside other specific tests like tonometry and ophthalmoscopic examinations. A member could point to it and ask if it's covered, so it is a real benefit.

## "Biomicroscopic evaluation" -> benefit (confidence=high)
- Biomicroscopic evaluation is a specific, nameable clinical procedure performed during an eye exam. It appears alongside other specific procedures (lid evaluation, ophthalmoscopy, tear test), confirming it is a concrete service a member could point to, not a generic category or fragment.

## "Birthing center" -> benefit (confidence=high)
- A birthing center is a specific, nameable facility/service that a member could ask whether it's covered. It refers to a concrete type of care setting, not a generic category word or a fragment/criterion.

## "Bite Splint" -> benefit (confidence=high)
- A bite splint (mandibular orthotic repositioning device) is a specific, nameable dental appliance a member could ask about coverage for. It names a concrete item, not a category or condition.

## "Bitewing radiographs (X-rays) and individual periapical films" -> benefit (confidence=high)
- This names specific dental diagnostic services -- bitewing X-rays and periapical films -- that a member could point to and ask if covered. It appears under Class I Diagnostic and Preventive Services, consistent with a specific nameable benefit.

## "Bleeding or clotting abnormalities" -> fragment_or_criterion (confidence=high)
- This is a medical condition listed as an example of criteria that justify facility/anesthesia services for dental care, not a nameable covered service or item itself. It describes a qualifying clinical condition, making it a criterion rather than a benefit.

## "Blended Lenses" -> benefit (confidence=high)
- Blended lenses are a specific, nameable optical product (a type of multifocal lens without a visible line). It appears in an exclusion list but names a real item, so it qualifies as a benefit regardless of coverage status.

## "Blepharoplasty of upper lids" -> benefit (confidence=high)
- Blepharoplasty of upper lids is a specific, nameable surgical procedure. It appears in a list alongside other specific surgeries (breast reduction, panniculectomy), confirming it names a concrete service a member could ask about.

## "Blood glucose monitors" -> benefit (confidence=high)
- 'Blood glucose monitors' is a specific, nameable medical item/supply covered under the diabetes management program. A member could point to it and ask if it's covered. This is a clear benefit.

## "Blood glucose monitors for the legally blind" -> benefit (confidence=high)
- This names a specific, tangible medical item -- blood glucose monitors designed for the legally blind -- listed among concrete diabetes supplies. A member could point to it and ask if it's covered. The qualifier 'for the legally blind' describes a specific product variant, not an eligibility criterion applied to a generic service.

## "Bone Marrow Transplants" -> benefit (confidence=high)
- Bone marrow transplants is a specific, nameable medical procedure that a member could ask about coverage for. It appears under Transplant Services and describes a concrete service, not a generic category or fragment.

## "Bone marrow" -> benefit (confidence=medium)
- The name 'Bone marrow' refers to a specific, nameable item/service in the context of transplants and donor searches. While the excerpts show it within a phrase ('Bone Marrow Donor Program Registry'), bone marrow transplantation is a real, specific covered service. It is not a generic administrative category nor a fragment/criterion. Leaning toward benefit given uncertainty about exact phrasing.

## "Bone marrow (described below)" -> benefit (confidence=medium)
- Under 'Transplant Services', 'Bone marrow' refers to a bone marrow transplant, which is a specific, nameable covered service. The '(described below)' is a cross-reference artifact but the core name refers to a real service. Leaning toward benefit.

## "Bone replacement grafts" -> benefit (confidence=high)
- This names a specific, nameable dental procedure (bone replacement grafts) listed among periodontal/surgical services. A member could point to it and ask if it's covered.

## "Breast reduction" -> benefit (confidence=high)
- Breast reduction is a specific, nameable surgical procedure listed among other concrete surgeries under the Surgery section. A member could clearly ask whether it is covered.

## "Bridges" -> benefit (confidence=medium)
- 'Bridges' refers to dental bridges, a specific, nameable dental prosthetic/service a member could ask about. Though the header lists it under diagnostic/preventive (bridges are usually major services), the name itself denotes a concrete service, so it qualifies as a benefit.

## "Broken or Lost Lenses or Frames" -> benefit (confidence=medium)
- The name refers to replacement of broken or lost lenses or frames, which is a specific, nameable service item a member could ask about (even though it appears in exclusion lists). It names a concrete item/service rather than a generic category or a mere condition/qualifier.

## "By a lab at your in- network physician’s direction." -> fragment_or_criterion (confidence=high)
- The name 'By a lab at your in-network physician's direction' describes a condition/scenario under which lab services are performed, not a specific nameable service. It's a qualifier fragment, not a benefit.

## "By a lab at your physician’s direction." -> fragment_or_criterion (confidence=high)
- The name 'By a lab at your physician's direction' does not name a specific service or item; it describes a condition/qualifier about how or where a service is performed. This is a fragment describing a scenario, not a nameable benefit.

## "By your physician, or" -> fragment_or_criterion (confidence=high)
- The name 'By your physician, or' is a sentence fragment describing a condition or qualifier (who performs/orders the service), not a specific nameable service. It has no service name in it.

## "Cardiovascular Management Program" -> benefit (confidence=high)
- This is a specific, nameable program under the Enhanced Condition Management Program that provides select services, equipment, and tools to manage hypertension. A member could point to it and ask if it's covered. It names a specific service offering rather than a generic category or a fragment/criterion.

## "Care for mental illness" -> benefit (confidence=medium)
- "Care for mental illness" names a specific, identifiable service (treatment/care for mental illness) that a member could ask about, even though here it appears in an exclusion list under Skilled Nursing Facility Services. Coverage/exclusion status must not drive classification. It is not a generic category word like 'Equipment' nor a fragment/criterion; it names an actual service type.

## "Care for senility or developmental disability" -> benefit (confidence=medium)
- This names a specific type of care (care for senility or developmental disability), parallel to sibling items like 'Custodial care', 'Care for substance use disorder', and 'Care for mental illness', which are nameable services. It appears in exclusion lists, but exclusion status must not drive classification. A member could point to it and ask if it's covered. It's a specific, nameable service type rather than a generic category or fragment.

## "Care for substance use disorder" -> benefit (confidence=high)
- 'Care for substance use disorder' names a specific, nameable service that a member could ask about. It appears alongside other real services like 'Custodial care' and 'Care for mental illness'. It happens to appear in an exclusion list under Skilled Nursing Facility context, but exclusion status must not influence classification.

## "Catheterization equipment and urinary sets" -> benefit (confidence=high)
- This names a specific, identifiable medical supply item (catheterization equipment and urinary sets) that a member could ask about coverage for. Although it appears under the generic 'Medical Supplies' header, the name itself refers to a concrete, nameable item rather than a generic category or a criterion/fragment.

## "Certified Nurse Anesthetist" -> benefit (confidence=high)
- A Certified Nurse Anesthetist is a specific, nameable provider/service that a member could ask about coverage for. Despite the odd section header, the name itself clearly refers to a specific service provider, not a generic category or fragment.

## "Certified Nurse Anesthetist (CRNA)" -> benefit (confidence=high)
- A Certified Nurse Anesthetist (CRNA) is a specific, nameable type of provider/service that a member could ask about coverage for. It names a real service item despite appearing under an unexpected header.

## "Certified Nurse Practitioner" -> benefit (confidence=medium)
- This names a specific type of provider (Certified Nurse Practitioner). While it's a provider type rather than a service, it's a specific, nameable entity that a member could reference. However, it functions more as a provider category than a specific covered service, so confidence is medium. Leaning toward benefit since it's a specific, nameable item.

## "Certified by the Michigan Department of Community Health" -> fragment_or_criterion (confidence=high)
- This is a certification requirement/eligibility criterion for a provider, not a nameable service. The excerpts show it as one of the conditions that training 'must be' certified by, describing a qualifier rather than a covered service.

## "Certified licensed social workers" -> fragment_or_criterion (confidence=medium)
- This names a type of provider (a professional category), not a specific covered service or item. It appears in a list of provider types (certified nurse practitioners, psychologists, physical therapists), which describes who renders care rather than a nameable benefit a member could ask 'is this covered?'. It's not a generic cost-share/process word, but it is a provider-designation qualifier rather than a service.

## "Certified to receive Medicare or Medicaid reimbursement or" -> fragment_or_criterion (confidence=high)
- The text 'Certified to receive Medicare or Medicaid reimbursement or' is a provider qualification criterion, not a nameable service. The excerpts show it describing requirements the provider of self-management training must meet. It names no specific covered service or item.

## "Cervical cancer screening" -> benefit (confidence=high)
- Cervical cancer screening is a specific, nameable preventive service that a member could ask about coverage for. It appears in a list of concrete preventive screenings.

## "Chemical profile" -> benefit (confidence=high)
- 'Chemical profile' is a specific, nameable laboratory test (a blood chemistry panel) listed as a routine screening service alongside cholesterol testing and colonoscopy under Preventive Care Services. A member could ask 'is this covered?' It names a specific service, not a category or fragment.

## "Chemotherapeutic drugs." -> benefit (confidence=high)
- Chemotherapeutic drugs is a specific, nameable class of medications used for cancer treatment. A member could clearly ask whether these are covered. It is not a generic administrative category nor a fragment/criterion.

## "Chemotherapy Infusion Pumps" -> benefit (confidence=high)
- The name refers to a specific, nameable durable medical equipment item -- chemotherapy infusion pumps -- which a member could point to and ask if covered. The section header seems mismatched but the name itself clearly names a concrete service/item.

## "Chemotherapy Prior Authorization" -> fragment_or_criterion (confidence=low)
- The name combines 'Chemotherapy' (a real service) with 'Prior Authorization,' which is an administrative process/requirement rather than a service. This appears to describe a process step or requirement for chemotherapy coverage rather than naming a specific coverable service. However, with no excerpt and only the name to judge from, confidence is low; it could arguably be a process/administrative item, but it reads more like a criterion/requirement than a nameable service.
- **Not auto-flagged**: below the high/medium-confidence precision gate.

## "Chemotherapy Specialty Pharmaceuticals" -> benefit (confidence=high)
- This names a specific, nameable category of covered items -- chemotherapy specialty pharmaceuticals/drugs. A member could ask 'are these covered?' It refers to a concrete drug type, not a generic process word like 'Drugs' alone or a fragment/criterion.

## "Chemotherapy for Bone Marrow Transplants" -> benefit (confidence=high)
- The name refers to a specific, nameable medical service -- chemotherapy administered in connection with bone marrow transplants -- under the Transplant Services section. A member could clearly ask whether this specific service is covered.

## "Chemotherapy for Oncology Clinical Trials" -> benefit (confidence=medium)
- The name refers to a specific, nameable service -- chemotherapy provided in the context of oncology clinical trials. A member could ask whether this is covered. It is not a generic category word nor a fragment/criterion. No excerpts available, but the name and header support classifying as a benefit.

## "Chiropractic Services" -> benefit (confidence=high)
- Chiropractic Services is a real, specific, nameable service a member could ask about coverage for. The section header mismatch (Chemotherapy) appears to be an extraction artifact, but the name itself clearly refers to a concrete service.

## "Chiropractic office visits:" -> benefit (confidence=high)
- 'Chiropractic office visits' names a specific, nameable service that a member could ask about coverage for. It appears under a clear chiropractic services header with specific coverage terms (one office visit every 36 months for new patients), confirming it is a concrete benefit rather than a generic category or fragment.

## "Cholesterol testing" -> benefit (confidence=high)
- Cholesterol testing is a specific, nameable diagnostic screening service that a member could ask about. It appears as a distinct item under Preventive Care Services.

## "Chronic, irreversible kidney failure (End Stage Renal Disease (ESRD))" -> benefit (confidence=medium)
- The name refers to a specific, nameable medical condition (End Stage Renal Disease) treated under the Dialysis Services benefit. Although phrased as a diagnosis rather than a service, it identifies a concrete condition a member could ask about coverage for, appearing under a specific benefit header. Leaning toward benefit per guidance, with medium confidence given it reads more like a diagnosis label than a service name.

## "Clinical Nurse Specialist-Certified" -> benefit (confidence=medium)
- 'Clinical Nurse Specialist-Certified' names a specific type of provider/practitioner whose services can be covered. Provider types are typically treated as nameable benefit categories in these certificates. It is not a generic process word nor a fragment/criterion. Confidence is medium due to lack of direct excerpts.

## "Co-culture of embryo(s)" -> benefit (confidence=high)
- Co-culture of embryo(s) is a specific, nameable medical/laboratory procedure used in assisted reproduction. A member could ask whether it is covered. It is not a generic category or a fragment/criterion.

## "Coating/Laminating" -> benefit (confidence=medium)
- Coating/laminating is a specific, nameable vision benefit -- a lens treatment/add-on service a member could ask about being covered. It names a concrete item/service rather than a category word or a fragment/criterion.

## "Collection of mature eggs and sperm" -> benefit (confidence=high)
- This names a specific, concrete medical service (collection of mature eggs and sperm) under fertility preservation. A member could point to it and ask if it's covered. It is not a generic category word or a fragment/criterion.

## "Colonoscopy" -> benefit (confidence=high)
- Colonoscopy is a specific, nameable medical procedure that a member could ask about coverage for. It appears as a distinct benefit under Preventive Care Services with defined coverage terms.

## "Complete dentures" -> benefit (confidence=high)
- 'Complete dentures' is a specific, nameable dental prosthetic device/service that a member could ask about. It appears under Class III Major Services with specific frequency limits, clearly a real benefit.

## "Composite Fillings" -> benefit (confidence=high)
- Composite fillings are a specific, nameable dental service used to repair decayed or damaged teeth. A member could clearly ask if they are covered. This is a real benefit.

## "Compounded hormones" -> benefit (confidence=high)
- Compounded hormones is a specific, nameable pharmaceutical product/service that a member could ask about. It appears in exclusion lists, but coverage status doesn't affect classification. It names a real, specific item.

## "Computerized axial tomography (CAT) scans" -> benefit (confidence=high)
- CAT scans are a specific, nameable diagnostic imaging service under Radiology Services that a member could ask about coverage for.

## "Conditions caused by accidental injuries, and" -> fragment_or_criterion (confidence=high)
- The name 'Conditions caused by accidental injuries, and' is a sentence fragment ending in 'and', describing a category of conditions rather than naming a specific, nameable service. It reads as a partial clause pulled from a longer sentence, not a benefit.

## "Consultations by dentists not providing treatment" -> benefit (confidence=medium)
- This names a specific, identifiable dental service—a consultation performed by a dentist who is not the one providing treatment (i.e., a second-opinion/specialist consultation). A member could point to it and ask whether it's covered. It appears alongside other real services like 'House and hospital calls' and 'Antibiotic injections' under Class II Basic Services. It's not a generic category word nor a bare condition/qualifier.

## "Consultations, Inpatient or Outpatient" -> benefit (confidence=medium)
- A consultation, whether inpatient or outpatient, is a specific, nameable medical service a member could ask about being covered. The inpatient/outpatient distinction is a setting qualifier but the core term 'Consultations' names a real service. Medium confidence due to lack of direct snippets.

## "Contact lenses every 12 months" -> benefit (confidence=high)
- 'Contact lenses' is a specific, nameable covered vision item; the 'every 12 months' is a frequency qualifier but the core names a real service/item a member could ask about. Appears in a covered benefits list in a vision certificate.

## "Continuous Positive Airway Pressure (CPAP)" -> benefit (confidence=high)
- CPAP is a specific, nameable piece of durable medical equipment used to treat sleep apnea. A member could clearly ask 'is CPAP covered?' It appears under Durable Medical Equipment and names a specific item, not a generic category or a fragment.

## "Continuous glucose monitor sensors" -> benefit (confidence=high)
- 'Continuous glucose monitor sensors' is a specific, nameable medical supply item that a member could ask about coverage for. It appears in a list alongside other specific diabetic supplies (test strips, lancets, insulin delivery reservoirs), confirming it is a concrete item rather than a generic category or fragment.

## "Continuous glucose monitors" -> benefit (confidence=high)
- 'Continuous glucose monitors' is a specific, nameable medical device that appears in a list of diabetic supplies and devices alongside glucometers and test strips. A member could clearly ask whether this specific item is covered.

## "Contraceptive Counseling" -> benefit (confidence=high)
- Contraceptive counseling is a specific, nameable preventive care service a member could ask about being covered. The excerpts define it as 'a preventive service that helps you choose a contraceptive method,' confirming it is a real service, not a generic category or fragment.

## "Contraceptive Devices Injections, and Implants" -> benefit (confidence=high)
- The name refers to specific, nameable medical items/services -- contraceptive devices, injections, and implants -- listed under Preventive Care Services. A member could clearly ask whether these are covered. This is a real benefit, not a generic category or fragment.

## "Contraceptive Drugs" -> benefit (confidence=high)
- Contraceptive Drugs names a specific, identifiable category of covered medication that a member could point to and ask about coverage. While 'Drugs' alone would be generic, 'Contraceptive Drugs' specifies a concrete class of items/medications, making it a real nameable benefit.

## "Contraceptive Injections" -> benefit (confidence=high)
- Contraceptive injections name a specific, nameable medical service/item that a member could ask about being covered. It appears under Preventive Care Services, consistent with a real benefit.

## "Contraceptive Mobile App" -> benefit (confidence=high)
- 'Contraceptive Mobile App' is a specific, nameable item/service covered under preventive care, with a defined frequency limit (one per member per 12 months). It refers to a concrete covered item, not a category word or a fragment/criterion.

## "Cornea" -> benefit (confidence=high)
- 'Cornea' in the transplant services context refers to corneal transplant, a specific, nameable medical service/procedure. The excerpts explicitly list cornea alongside skin and bone marrow transplants as payable procedures. This is a real, specific benefit a member could ask about.

## "Cornea evaluation" -> benefit (confidence=high)
- Cornea evaluation is a specific, nameable diagnostic vision service listed alongside other specific tests (ophthalmoscopy, tear test, pupil evaluation). A member could ask whether it's covered.

## "Cosmetic Lenses/Processes" -> benefit (confidence=medium)
- The name refers to specific vision items/services -- cosmetic lens options and lens processing/coatings under the Contact Lenses section. These are nameable items a member could ask about coverage for, even if often excluded. Not a generic category word or a fragment/criterion. Medium confidence due to lack of direct excerpts.

## "Cosmetic Surgery" -> benefit (confidence=high)
- Cosmetic surgery is a specific, nameable medical service that a member could ask about. It appears under the Surgery section with conditions on when it's payable, but the name itself refers to a real, specific service regardless of coverage limitations.

## "Cosmetic surgery is only payable for:" -> fragment_or_criterion (confidence=high)
- The name 'Cosmetic surgery is only payable for:' is a sentence fragment introducing a list of conditions/criteria under which cosmetic surgery is covered. It does not itself name a specific service; the trailing colon and phrasing indicate it's a lead-in to eligibility criteria. While 'cosmetic surgery' is a real service, the extracted string is a qualifier clause, not a clean benefit name.

## "Counseling services" -> benefit (confidence=medium)
- 'Counseling services' names a specific, identifiable service a member could ask about being covered, listed alongside diagnostic and planning services under Infertility Treatment. While somewhat broad, it refers to a nameable service rather than a pure category/process word or a fragment/criterion.

## "Coverage Requirements" -> fragment_or_criterion (confidence=high)
- 'Coverage Requirements' is a heading introducing eligibility conditions (services must be medically necessary and appropriate), not a specific nameable service or item. It describes rules/criteria rather than a benefit.

## "Covered Drugs Obtained from an Out-of-Network Pharmacy" -> fragment_or_criterion (confidence=medium)
- The name describes a scenario/condition -- drugs obtained through a particular channel (an out-of-network pharmacy) -- rather than naming a specific covered service or item. The actual benefit is 'prescription drugs'; this phrase qualifies where/how they're obtained, making it a criterion/scenario rather than a nameable service.

## "Covered services and devices for pain management" -> benefit (confidence=medium)
- The name refers to a specific, nameable category of services and devices for pain management, which appears under a 'Pain Management' benefit section. While it uses somewhat generic 'covered services and devices' phrasing, it names a concrete clinical domain (pain management) that a member could point to and ask about. Leaning toward benefit given the specific service area.

## "Covered services are provided within the state of Michigan." -> fragment_or_criterion (confidence=high)
- The text describes a geographic eligibility condition ('Covered services are provided within the state of Michigan') under a list of criteria that must be met for coverage. It names no specific service; it is a qualifying condition, so it is a fragment/criterion.

## "Covered services include, but not limited to, the following:" -> fragment_or_criterion (confidence=high)
- This is an introductory clause ('Covered services include, but not limited to, the following:') that precedes a list of benefits. It does not name any specific service itself; it is a sentence fragment used as a list header, not a nameable benefit.

## "Crowns" -> benefit (confidence=high)
- 'Crowns' names a specific, nameable dental item/service that a member could ask about coverage for. It is not a generic category word or a fragment; it refers to a concrete dental restoration.

## "Cryopreservation of embryos, mature eggs and sperm" -> benefit (confidence=high)
- The name refers to a specific, nameable medical service -- cryopreservation of embryos, mature eggs and sperm -- under the Fertility Preservation section. A member could clearly ask whether this specific service is covered.

## "Culture of eggs" -> benefit (confidence=high)
- 'Culture of eggs' is a specific, nameable fertility preservation procedure appearing alongside other concrete services like 'Ovarian transposition' and 'Embryo transfer.' A member could point to it and ask if it's covered.

## "Custodial care" -> benefit (confidence=high)
- 'Custodial care' is a real, specific, nameable type of care service that a member could ask about. It appears in exclusion lists here, but the guidance explicitly cites 'Custodial care' as an example of a real benefit that happens to be excluded. Coverage status must not drive classification.

## "Custodial or nonskilled care" -> benefit (confidence=high)
- Custodial or nonskilled care is a specific, nameable type of care service that a member could ask about coverage for. Like 'Custodial care' example, it's a real service even though it appears in exclusion lists here. Coverage status must not drive classification.

## "Dailies (three-month supply)" -> benefit (confidence=medium)
- The name refers to daily disposable contact lenses provided as a three-month supply, which is a specific, nameable item a member could ask about under the Contact Lenses section of a vision plan. It names a concrete covered item rather than a generic category or a fragment/criterion.

## "Damage to the device so that it cannot be restored" -> fragment_or_criterion (confidence=high)
- This text describes a condition/scenario under which a prosthetic device may be replaced ('Damage to the device so that it cannot be restored'), listed alongside 'A change in the patient's condition' and 'Loss of the device'. It does not name a specific service or item; it is a qualifying circumstance/eligibility criterion for replacement.

## "Deemed safe and effective by BCBSM" -> fragment_or_criterion (confidence=high)
- The name 'Deemed safe and effective by BCBSM' describes a qualifying condition/criterion that a treatment must meet, not a specific nameable service. It appears as a bullet listing requirements for autism spectrum disorder treatments, making it a criterion rather than a benefit.

## "Dental Services in a Participating Hospital" -> benefit (confidence=medium)
- 'Dental Services in a Participating Hospital' names a specific, nameable category of covered service tied to a place of service. While 'Dental Services' alone might lean generic, the qualifier makes it a specific covered benefit a member could ask about. It is a real service offering rather than a cost-share, process word, or fragment/criterion.

## "Dental conditions existing before an accident requiring emergency dental treatment" -> fragment_or_criterion (confidence=medium)
- This describes a scenario/condition (pre-existing dental conditions that exist before an accident) rather than naming a specific service. It functions as a qualifier/exclusion clause describing which situations are not covered, not a nameable service a member could point to. The 'benefit' being referenced is really emergency dental treatment, with this being a condition-based limitation on it.

## "Dental injury" -> benefit (confidence=medium)
- The name 'Dental injury' (accidental dental injury) refers to a specific, nameable condition/service scenario — damage to the face or jaw from external force, with follow-up treatment covered. This is a specific, pointable item a member could ask about, rather than a generic category or a mere qualifier. The match appears to be a fragment of 'accidental injury' text, but the underlying concept of dental injury treatment is a real benefit. Leaning toward benefit per guidance.

## "Dental sealants" -> benefit (confidence=high)
- Dental sealants are a specific, nameable dental service that a member could point to and ask if covered. Appears in a list of specific services alongside space maintainers and X-rays.

## "Dental surgery is only payable for:" -> fragment_or_criterion (confidence=high)
- The candidate name 'Dental surgery is only payable for:' is a sentence lead-in introducing a list of conditions/criteria, not a specific nameable service. It describes when dental surgery is payable rather than naming the service itself.

## "Depo-Provera and Intrauterine Devices (IUD)" -> benefit (confidence=high)
- The name refers to specific, nameable contraceptive items/services (Depo-Provera injections and intrauterine devices), which members could clearly point to and ask if covered. Appearing under Preventive Care Services confirms it is a real benefit.

## "Devices ordered or purchased prior to the certificate’s effective date" -> fragment_or_criterion (confidence=high)
- The name describes a timing condition/exclusion scenario ('ordered or purchased prior to the certificate's effective date') rather than naming a specific covered device or service. It is a qualifier/criterion, not a nameable benefit item.

## "Diabetes Prevention Program" -> benefit (confidence=high)
- 'Diabetes Prevention Program' is a specific, nameable service/program that a member could ask about coverage for. The excerpts show it as a distinct program providing select services, equipment, and tools to reduce Type 2 diabetes risk.

## "Diabetic specialty shoes" -> benefit (confidence=high)
- 'Diabetic specialty shoes' names a specific, nameable item that a member could ask about being covered. It appears as a distinct bullet under the diabetes management program, clearly denoting a concrete covered item.

## "Diagnostic Radiology Services" -> benefit (confidence=high)
- Diagnostic Radiology Services names a specific, identifiable medical service (facility and physician radiology services used to diagnose). A member could point to it and ask if it's covered. It is more specific than a bare category like 'Radiology' and refers to a concrete nameable service.

## "Diagnostic Tests" -> generic_administrative (confidence=medium)
- "Diagnostic tests" is a generic category noun describing a type of diagnostic procedure rather than a specific, nameable service. It appears alongside "laboratory examinations" as a broad category. While in a dental context it's somewhat more specific, the name itself is generic. Leaning generic_administrative but with medium confidence given some borderline specificity.

## "Diagnostic X-rays" -> benefit (confidence=high)
- Diagnostic X-rays is a specific, nameable service a member could ask about coverage for. It refers to a concrete diagnostic imaging procedure, not a generic category or fragment.

## "Diagnostic agents" -> benefit (confidence=medium)
- Diagnostic agents are a specific, nameable category of pharmaceutical items (e.g., contrast media, diagnostic reagents) that a member could ask about. Though appearing in exclusion lists, coverage status must not drive classification. It names a real class of items rather than being a generic process word or a fragment/criterion.

## "Diagnostic and preventive services" -> generic_administrative (confidence=medium)
- This is a class/category grouping ('Class I – Diagnostic and Preventive Services') rather than a specific nameable service. It describes a broad category of dental services rather than a single service a member could point to. The name is a category label heading a group of individual benefits.

## "Diagnostic studies done for the sole purpose of infertility assessment" -> benefit (confidence=medium)
- This names a specific, identifiable service -- diagnostic studies for infertility assessment. Although it includes a qualifier ('for the sole purpose of infertility assessment'), the core is a nameable service (diagnostic studies) that a member could ask about. It appears in a bulleted list alongside other real services in the Infertility Treatment section. Coverage/exclusion status doesn't affect this being a real service.

## "Diagnostic tests and laboratory examinations" -> benefit (confidence=medium)
- Names a specific, nameable dental service (diagnostic tests and laboratory examinations) that a member could ask about, listed alongside other concrete services like dental sealants and space maintainers. Though somewhat category-like, it refers to identifiable diagnostic services rather than a pure administrative process word.

## "Diaphragms (when performed in the physician’s office)" -> benefit (confidence=high)
- The core name 'Diaphragms' refers to a specific, nameable contraceptive device/service, appearing under Preventive Care Services. The parenthetical qualifier is just a setting condition; the underlying item is a real benefit.

## "Dietary supplements" -> benefit (confidence=high)
- Dietary supplements is a specific, nameable item that a member could point to and ask about coverage. It appears in exclusion lists, but exclusion status does not affect classification. It names a real, specific category of items.

## "Diversional therapy" -> benefit (confidence=high)
- Diversional therapy is a specific, nameable therapeutic service (recreational/activity-based therapy). Although it appears in an exclusion list here, it names a real service, so it qualifies as a benefit regardless of coverage status.

## "Domiciliary foster care" -> benefit (confidence=high)
- Domiciliary foster care names a specific, identifiable type of care service that a member could ask about. Although it appears in exclusion lists (alongside custodial care), that does not affect classification. It is a nameable service, not a generic category or fragment.

## "Donor lymphocyte infusion" -> benefit (confidence=high)
- Donor lymphocyte infusion is a specific, nameable medical procedure used in transplant/oncology treatment. A member could ask whether it is covered. It appears alongside other specific transplant services in bulleted lists.

## "Double-blind food challenge test and bronchial challenge test" -> benefit (confidence=high)
- The name refers to specific, nameable diagnostic tests (double-blind food challenge and bronchial challenge tests) under allergy testing. A member could ask whether these are covered. This is a real, specific benefit.

## "Drugs" -> generic_administrative (confidence=high)
- 'Drugs' is a generic category noun appearing in a list alongside 'Equipment', 'Supplies', 'Solutions', and 'Other medically necessary services' — all generic category items describing kinds of provisions related to dialysis, not a specific nameable service or item a member could ask about.

## "Drugs Received in Other Locations" -> generic_administrative (confidence=medium)
- This is a category/location-based grouping heading ('Drugs Received in Other Locations') that organizes where drugs may be dispensed, rather than naming a specific covered drug or service. It functions as a sub-heading describing a category of provision, similar to generic administrative nouns like 'Drugs' or 'Other Services'.

## "Drugs Received in a Hospital" -> benefit (confidence=high)
- 'Drugs Received in a Hospital' names a specific, identifiable covered item -- prescription drugs, biologicals and solutions administered in a hospital setting. It is a concrete service category a member could point to and ask if covered, not a generic process word like bare 'Drugs' nor a fragment/criterion.

## "Drugs obtained from an out-of-network mail order provider." -> fragment_or_criterion (confidence=high)
- The name describes a scenario/condition -- drugs obtained through a particular channel (out-of-network mail order provider) -- rather than naming a specific covered service or item. It functions as an exclusion criterion, not a nameable benefit.

## "Drugs, biologicals and solutions" -> generic_administrative (confidence=medium)
- The name 'Drugs, biologicals and solutions' is a broad category grouping rather than a specific nameable service. It lists general classes of items provided during skilled nursing facility care, describing a kind of provision rather than a specific covered service a member could point to. Similar to 'Drugs' or 'Equipment' as generic category nouns.

## "Drugs, biologicals and solutions used in the facility" -> benefit (confidence=medium)
- The name refers to specific, nameable items -- drugs, biologicals, and solutions administered in the facility. While it describes a category of items, it names concrete medical supplies/items a member could ask about coverage for, similar to a covered supply benefit. It is not purely a generic process word like 'Coinsurance', nor a fragment/criterion. Leaning toward benefit given the specific nameable items.

## "Drugs, biologicals and solutions used including drugs taken home" -> benefit (confidence=medium)
- The name refers to a specific, nameable category of items -- drugs, biologicals, and solutions used during treatment, including take-home drugs. While it starts with the generic word 'Drugs', the full phrase describes a concrete set of items a member could point to and ask about coverage. It's not merely a process/category word like 'Drugs' alone, nor is it a fragment or eligibility criterion. Leaning toward benefit given the specific enumeration.

## "Drugs, biologicals and solutions, including drugs taken home" -> benefit (confidence=medium)
- The name refers to specific, nameable items -- drugs, biologicals, and solutions administered as part of care, including take-home drugs. This is a concrete covered item a member could ask about, not a generic category word or a fragment/criterion. While 'Drugs' alone would be generic, this fully specified phrase names particular items with qualifying detail, so it leans benefit.

## "EKGs" -> benefit (confidence=high)
- EKGs (electrocardiograms) are a specific, nameable diagnostic service a member could ask about being covered. It appears in a service list under Surgery, naming a concrete item/service.

## "Eight visits for children from birth through 12 months" -> fragment_or_criterion (confidence=high)
- This is a quantity/frequency limitation sub-bullet under the actual benefit 'Well-Baby and Well-Child Visits'. It describes a visit allowance for an age range rather than naming a specific service. It's a criterion/limitation, not a nameable benefit.

## "Electricity or water used to operate the dialyzer" -> fragment_or_criterion (confidence=medium)
- 'Electricity or water used to operate the dialyzer' describes utility costs/ancillary items associated with dialysis rather than naming a specific covered medical service. It reads as an exclusion-type line item describing incidental costs, not a nameable benefit a member would point to and ask 'is this covered.' It's more of a qualifier/scenario item than a distinct service.

## "Electrocardiogram (EKG)" -> benefit (confidence=high)
- An electrocardiogram (EKG) is a specific, nameable diagnostic service that a member could ask about coverage for. It appears under 'Diagnostic Services', consistent with a real benefit.

## "Electroconvulsive Therapy (ECT)" -> benefit (confidence=high)
- Electroconvulsive Therapy (ECT) is a specific, nameable medical/behavioral health treatment that a member could ask about coverage for. It appears under Behavioral Health Services and refers to a concrete procedure, not a category or a criterion.

## "Electroconvulsive Treatment (ECT)" -> benefit (confidence=high)
- Electroconvulsive Treatment (ECT) is a specific, nameable medical procedure used to treat certain psychiatric conditions. A member could clearly ask whether it is covered, making it a real benefit rather than a generic category or fragment.

## "Electroencephalogram (EEG)" -> benefit (confidence=high)
- An electroencephalogram (EEG) is a specific, nameable diagnostic procedure that a member could ask about coverage for. It appears under 'Diagnostic Services' and clearly names a concrete medical service.

## "Electromyogram (EMG)" -> benefit (confidence=high)
- An electromyogram (EMG) is a specific, nameable diagnostic test that a member could ask about coverage for. It appears under Diagnostic Services, consistent with a real benefit.

## "Embryo transfer to member within one year from cryopreservation" -> benefit (confidence=high)
- 'Embryo transfer' is a specific, nameable medical procedure a member could ask about. The temporal qualifier ('within one year from cryopreservation') is a coverage condition, but the core names a real service. It appears in a covered-services list under Fertility Preservation alongside other specific procedures like 'Culture of eggs' and 'Ovarian transposition'.

## "Emergency Dental Care" -> benefit (confidence=high)
- 'Emergency Dental Care' is a specific, nameable service a member could ask about coverage for. The excerpts describe where the service is provided and that it is paid for, confirming it is a real benefit.

## "Emergency palliative treatment" -> benefit (confidence=high)
- Emergency palliative treatment is a specific, nameable dental service providing temporary pain relief, listed as a covered service in dental benefit classes. A member could point to it and ask if it's covered.

## "Endodontic Services" -> benefit (confidence=high)
- Endodontic services is a specific, nameable dental service category (root canals, treating diseased/damaged nerves) that a member could ask about coverage for. It refers to a concrete type of dental treatment, not a generic administrative process.

## "Enhanced Diabetes Management Program" -> benefit (confidence=high)
- 'Enhanced Diabetes Management Program' is a specific, nameable program/service providing select services, equipment, and tools to manage Type 2 diabetes. A member could point to it and ask if it's covered. It is not a generic category word nor a fragment/criterion.

## "Environmental studies, evaluation, or control" -> benefit (confidence=medium)
- Under an 'Allergy Testing and Therapy' header, 'Environmental studies, evaluation, or control' names a specific type of allergy-related service (assessment/control of environmental allergens). It refers to a nameable service a member could ask about, so it qualifies as a benefit rather than a generic category or fragment, though the somewhat category-like phrasing lowers confidence.

## "Equipment" -> generic_administrative (confidence=high)
- 'Equipment' is a generic category noun, not a specific nameable service. In the excerpts it appears as part of 'services, supplies and equipment to treat' dialysis conditions, describing a kind of provision rather than a specific covered item a member could point to.

## "Evaluations or tests, including the Autism Diagnostic Observation Schedule" -> benefit (confidence=medium)
- The name refers to specific, nameable diagnostic services for autism spectrum disorders, including the Autism Diagnostic Observation Schedule (a real, named assessment tool). A member could ask whether these evaluations/tests are covered. While it starts somewhat generically ('Evaluations or tests'), the inclusion of a specific named diagnostic instrument makes it a concrete service rather than a pure category word or fragment.

## "Excision of hyperplastic tissue per arch" -> benefit (confidence=high)
- This names a specific, nameable dental surgical procedure (excision of hyperplastic tissue per arch), listed alongside other specific procedures like removal of exostoses and frenulectomies. A member could point to it and ask if it's covered.

## "Experimental equipment" -> benefit (confidence=medium)
- 'Experimental equipment' names a specific, identifiable category of equipment that a member could point to and ask about coverage. It appears in an exclusion list, but exclusion status must not drive classification. While somewhat generic, it refers to a nameable item type rather than a pure process/cost-share word, so it leans toward benefit.

## "Experimental prosthetic devices" -> benefit (confidence=high)
- 'Experimental prosthetic devices' names a specific, nameable item (prosthetic devices that are experimental). A member could point to it and ask if it's covered. It appears in an exclusion list, but exclusion status must not drive classification. This is a real, specific item, not a generic category word or a bare fragment/criterion.

## "Experimental treatment not included in this certificate" -> fragment_or_criterion (confidence=high)
- The name 'Experimental treatment not included in this certificate' does not name a specific service; it describes a qualifier/exclusion scenario. The phrase 'not included in this certificate' is a condition rather than a nameable service item.

## "External exams of the eye" -> benefit (confidence=medium)
- 'External exams of the eye' names a specific, nameable diagnostic service/procedure component of an eye exam. A member could point to it as a defined service. While it appears as a component within a required exam list, it refers to an actual clinical examination rather than an administrative category or a condition/qualifier.

## "FDA approved" -> fragment_or_criterion (confidence=high)
- 'FDA approved' is a qualifying condition that injectable/infused drugs must meet, not a specific nameable service. The excerpts show it as a bullet in a list of criteria (must be FDA approved, ordered by a physician, etc.), making it an eligibility criterion rather than a benefit.

## "Family counseling" -> benefit (confidence=high)
- 'Family counseling' is a specific, nameable behavioral health service that a member could ask whether it's covered. It appears alongside other specific services like individual psychotherapy and psychological testing.

## "Fecal Occult Blood Screening" -> benefit (confidence=high)
- Fecal Occult Blood Screening is a specific, nameable diagnostic test that a member could point to and ask if it's covered. It appears under Preventive Care Services with clear service definition (one per member per calendar year to detect blood in feces/stool).

## "Five days of occasional respite care during a 30-day period" -> fragment_or_criterion (confidence=medium)
- The name 'Five days of occasional respite care during a 30-day period' describes a quantity/limitation on respite care rather than naming a service. The underlying service is 'respite care,' but this candidate is phrased as a coverage limit/scenario ('five days...during a 30-day period'), which reads as a criterion or limitation description rather than a clean benefit name. Leaning toward fragment_or_criterion but with only medium confidence since it does reference a real service.

## "Fluorescein evaluation" -> benefit (confidence=high)
- Fluorescein evaluation is a specific, nameable diagnostic vision service (a corneal/tear film test using fluorescein dye), appearing alongside other specific evaluations like cornea evaluation and lid evaluation. A member could point to it and ask if it's covered.

## "Fluoride treatments" -> benefit (confidence=high)
- Fluoride treatments is a specific, nameable dental service listed under diagnostic and preventive services. A member could clearly ask 'is this covered?'

## "For bone marrow transplants" -> fragment_or_criterion (confidence=medium)
- The name 'For bone marrow transplants' is a prepositional phrase fragment, part of a subheading 'Additional services for bone marrow transplants'. While bone marrow transplant is a real service, the extracted text itself is a fragment/qualifier ('for...') rather than a clean service name. It reads as a scoping phrase introducing additional services rather than naming the benefit.

## "For oncology clinical trials" -> fragment_or_criterion (confidence=medium)
- The name 'For oncology clinical trials' is a prepositional fragment ('For...'), not a nameable service. While 'oncology clinical trials' itself could be a benefit, the extracted candidate is phrased as a qualifier/scenario clause rather than a specific service name. It reads as introducing conditions applicable to oncology clinical trials rather than naming a service a member could point to.

## "Frenulectomies" -> benefit (confidence=high)
- A frenulectomy is a specific, nameable surgical dental procedure (removal of a frenulum). It appears in a list of specific surgical services under Class III Major Services, making it a real benefit.

## "Full-mouth and panoramic radiographs (X ‐ rays)" -> benefit (confidence=high)
- This names a specific, identifiable dental service -- full-mouth and panoramic X-rays -- appearing under a Basic Services class. A member could clearly ask 'is this covered?' It is a concrete nameable diagnostic item, not a generic category or fragment.

## "Gender affirming surgery and related services" -> benefit (confidence=high)
- 'Gender affirming surgery and related services' names a specific, identifiable medical service that a member could ask about. It appears as a distinct bulleted covered service under Gender Affirming Services, not as a category process word or a conditional fragment.

## "General Anesthesia" -> benefit (confidence=high)
- General anesthesia (or IV sedation) in connection with oral surgery is a specific, nameable service a member could ask about. It is a concrete covered item, not a generic category or a fragment.

## "General housekeeping services" -> benefit (confidence=medium)
- 'General housekeeping services' names a specific, identifiable type of service that a member could ask about, appearing alongside other nameable services like transportation and private duty nursing in an exclusion list. Its exclusion status does not affect classification. It is a nameable service rather than a category/process word or a fragment/criterion.

## "General nursing services" -> benefit (confidence=medium)
- 'General nursing services' names a specific, identifiable service provided in a residential treatment facility that a member could point to and ask about. While somewhat broad, it refers to an actual nameable service (nursing care) rather than a pure administrative category or a fragment/criterion. Leaning toward benefit per guidance when uncertain.

## "Genetic counselling and breast cancer genetic testing (BRCA)" -> benefit (confidence=high)
- The name refers to specific, nameable services: genetic counselling and BRCA breast cancer genetic testing. A member could clearly ask whether this is covered. It appears under Preventive Care Services, consistent with a real benefit.

## "Genetic testing" -> benefit (confidence=high)
- Genetic testing is a specific, nameable medical service that a member could ask about coverage for. It appears in a bulleted list of covered services under Autism Spectrum Disorders alongside other clear benefits like outpatient mental health therapy and nutritional therapy.

## "Gingival flap procedures" -> benefit (confidence=high)
- Gingival flap procedures is a specific, nameable dental/periodontal surgical procedure. It appears alongside other specific services like soft tissue grafts and osseous surgeries under Major Services, and a member could clearly ask whether it's covered.

## "Gingivectomies and gingivoplasties" -> benefit (confidence=high)
- Gingivectomies and gingivoplasties are specific, nameable dental surgical procedures (removal/reshaping of gum tissue). They appear in a list of specific periodontal services under Class III Major Services, and a member could clearly point to them and ask if covered.

## "Glucometers" -> benefit (confidence=high)
- Glucometers is a specific, nameable medical device (blood glucose meter) listed as a diabetic supply. A member could point to it and ask if it's covered. This is a concrete item, not a generic category or fragment.

## "Group psychotherapeutic treatment" -> benefit (confidence=high)
- Group psychotherapeutic treatment is a specific, nameable behavioral health service that appears in lists alongside other distinct services like individual psychotherapy and psychological testing. A member could clearly ask whether it is covered.

## "HIV counseling and screening" -> benefit (confidence=high)
- HIV counseling and screening is a specific, nameable preventive service that appears in a preventive care benefits list alongside other specific screenings. A member could clearly ask whether it's covered.

## "HPV screening" -> benefit (confidence=high)
- HPV screening is a specific, nameable preventive service that a member could ask whether it's covered. It appears in a list of concrete preventive screenings under Preventive Care Services.

## "Hair prostheses such as wigs, hair pieces, hair implants, etc." -> benefit (confidence=high)
- The name refers to a specific, nameable item -- hair prostheses (wigs, hair pieces, hair implants). A member could point to it and ask if it's covered. It appears under a Prosthetic and Orthotic Devices header, consistent with a real device benefit, regardless of coverage status.

## "Health Maintenance Examination" -> benefit (confidence=high)
- A health maintenance examination is a specific, nameable preventive care service that a member could point to and ask if it's covered. It has defined limits (one exam per member per calendar year) and is a real service, not a generic category or fragment.

## "Hearing aids" -> benefit (confidence=high)
- Hearing aids is a specific, nameable item a member could ask about coverage for. It appears as a bulleted item under Prosthetic and Orthotic Devices. Real benefit regardless of coverage status.

## "Hemisections" -> benefit (confidence=high)
- Hemisection is a specific, nameable dental surgical procedure (surgical removal/separation of one root of a multi-rooted tooth). It appears as a distinct service item under Major Services, making it a real benefit.

## "Hi index lenses" -> benefit (confidence=high)
- High index lenses are a specific, nameable lens option under vision coverage that a member could ask about, regardless of coverage status.

## "High-dose chemotherapy and/or total body irradiation" -> benefit (confidence=high)
- The name refers to specific, nameable medical services -- high-dose chemotherapy and total body irradiation -- commonly provided in transplant and oncology contexts. Despite its length, it names concrete procedures a member could ask about, and it appears under relevant clinical section headers.

## "History" -> fragment_or_criterion (confidence=medium)
- 'History' here is a component of what an eye exam must include, not a standalone nameable benefit a member would ask about. It's a sub-item/element of the exam process rather than a specific covered service. It's a fragment describing a required exam component.

## "Home hemodialysis" -> benefit (confidence=high)
- Home hemodialysis is a specific, nameable medical service (dialysis performed at home) that a member could point to and ask if it's covered. It appears under 'Dialysis Services' as a covered item with specific sub-details, confirming it is a real benefit.

## "Hospital (inpatient or outpatient)" -> generic_administrative (confidence=medium)
- The name 'Hospital (inpatient or outpatient)' describes a place/setting of care and a category of service delivery rather than a specific nameable covered service. Under a 'Surgery' header it appears to indicate where surgery is performed rather than naming a particular procedure or benefit. This reads as a category/setting noun, not a specific service a member would point to and ask if covered.

## "Hospitalization" -> generic_administrative (confidence=high)
- "Hospitalization" is a generic category/process noun describing the kind of care setting rather than a specific nameable service. It appears as a sub-item under transplant services listing components of care, but the word itself is a broad administrative category, not a specific benefit like 'high-dose chemotherapy' or 'bone marrow infusion' listed alongside it.

## "Hospitals and Other Facilities" -> generic_administrative (confidence=high)
- This is a category heading grouping provider types (hospitals and other facilities) rather than a specific nameable covered service. It describes the kind of provider/facility, not a particular benefit a member could point to and ask about.

## "House and hospital calls" -> benefit (confidence=high)
- This names a specific, nameable dental service -- calls/visits made by a dentist at a house or hospital. It appears in a list of specific Class II basic services alongside consultations, antibiotic injections, etc. A member could point to it and ask if it's covered.

## "Housekeeping items and services" -> generic_administrative (confidence=medium)
- 'Housekeeping items and services' is a generic category noun describing a kind of ancillary support (cleaning/facility maintenance) rather than a specific, nameable covered medical service. It appears in a list of ancillary items associated with surgery facility services, functioning as a broad category label rather than a distinct benefit a member would point to and ask 'is this covered?'

## "Hyperbaric oxygenation (therapy given in a pressure chamber)" -> benefit (confidence=high)
- Hyperbaric oxygenation is a specific, nameable medical therapy delivered in a pressure chamber. It's a concrete service a member could ask about, listed under Hospital Services. Clearly a benefit.

## "IV Sedation" -> benefit (confidence=high)
- IV sedation is a specific, nameable service provided in connection with oral surgery. A member could point to it and ask if it's covered. It's not a generic category or a fragment/criterion.

## "Immunizations" -> benefit (confidence=high)
- Immunizations/vaccines are a specific, nameable covered service that a member could point to and ask if covered. Excerpts describe paying for specific vaccines against infection, confirming it names a real service.

## "In a participating skilled nursing facility (see Page 118)" -> fragment_or_criterion (confidence=high)
- The name is a prepositional phrase describing a location/scenario ('In a participating skilled nursing facility') with a cross-reference to another page. It does not name a specific service or item; it describes where a benefit applies rather than being a benefit itself.

## "In vitro fertilization" -> benefit (confidence=high)
- In vitro fertilization is a specific, nameable medical procedure that a member could ask about coverage for. It appears in a bulleted list of distinct infertility services, confirming it's a concrete service rather than a category or fragment.

## "Individual and group therapy or counseling" -> benefit (confidence=high)
- This names a specific, identifiable behavioral health service (individual and group therapy or counseling) that a member could point to and ask if it's covered. It appears alongside other specific services like psychological testing and family therapy under Behavioral Health Services.

## "Individual psychotherapeutic treatment" -> benefit (confidence=high)
- Individual psychotherapeutic treatment names a specific, nameable mental health service that a member could ask about coverage for. It appears alongside other specific services like family counseling and psychological testing, confirming it's a distinct benefit rather than a category or fragment.

## "Infertility testing and treatment" -> benefit (confidence=high)
- 'Infertility testing and treatment' names a specific, nameable medical service a member could ask about coverage for. It appears alongside other clear benefits like bariatric surgery and prosthetics/orthotics. Though somewhat broad, it refers to a concrete category of covered medical services, not an administrative process word or a fragment/criterion.

## "Infusion of bone marrow and/or peripheral blood stem cells" -> benefit (confidence=high)
- This names a specific, identifiable medical procedure -- the infusion of bone marrow and/or peripheral blood stem cells, a concrete transplant-related service under Transplant Services. A member could clearly ask whether this specific procedure is covered.

## "Infusion of colony stimulating growth factors" -> benefit (confidence=high)
- This names a specific, nameable medical service -- the infusion of colony stimulating growth factors, a concrete procedure used in transplant contexts. A member could point to it and ask if it's covered. It is not a generic category word or a fragment/criterion.

## "Infusion pumps" -> benefit (confidence=high)
- Infusion pumps is a specific, nameable medical device/item a member could ask about coverage for, used for administration of chemotherapy. It is a concrete item, not a category word or fragment.

## "Inhalation therapy" -> benefit (confidence=high)
- Inhalation therapy is a specific, nameable medical service that a member could ask about coverage for. It appears in a list alongside other specific services like ECT and pulmonary function evaluation.

## "Injectable/Infused Drugs" -> benefit (confidence=medium)
- The name refers to a specific category of medications administered by injection or infusion, which is a nameable, pointable service a member could ask about coverage for. While somewhat broad, injectable/infused drugs is a recognized specific benefit type distinct from oral prescription drugs, not merely a generic process word.

## "Injections of antiallergen, antihistamine, bronchodilator or antispasmodic agents" -> benefit (confidence=high)
- The name refers to a specific, nameable medical service -- injections of specific pharmacological agents (antiallergen, antihistamine, bronchodilator, antispasmodic) -- under the Allergy Testing and Therapy section. A member could clearly ask 'is this injection covered?' This is a concrete service, not a category word or a fragment.

## "Inlays" -> benefit (confidence=high)
- Inlays are a specific, nameable dental restoration that a member could point to and ask if covered. They appear alongside crowns, veneers, and onlays as concrete dental items. This is a real dental service/item, not a generic category or fragment.

## "Inpatient Hospital" -> generic_administrative (confidence=high)
- 'Inpatient Hospital' is a care setting/category noun rather than a specific nameable service. The actual services (e.g. 'Acute detoxification') are listed as sub-bullets under it. It describes the kind of setting, not a specific covered service.

## "Inpatient Hospital Mental Health Services" -> benefit (confidence=high)
- This names a specific, identifiable service - inpatient hospital mental health services - that a member could point to and ask if it's covered. It includes specific treatments like individual psychotherapy. It is a nameable service, not a generic category word or fragment.

## "Inpatient Hospital Services:" -> generic_administrative (confidence=high)
- This is a category heading ('Inpatient Hospital Services:') that introduces a sub-list of actual services (medical care by hospital personnel, etc.). It describes a kind/category of provision rather than a specific nameable service, and the colon plus following sub-bullets confirm it's a grouping header.

## "Inpatient admissions that BCBSM has not preapproved" -> fragment_or_criterion (confidence=high)
- The name describes a condition/scenario (admissions lacking preapproval) rather than naming a specific service. It's an exclusion criterion qualifying inpatient admissions, not a nameable benefit itself.

## "Insulin" -> benefit (confidence=high)
- Insulin is a specific, nameable medical item/drug that a member could ask about coverage for. It appears in the diabetes management supply lists (e.g. 'Insulin pumps') and is clearly a concrete covered item, not a generic category or fragment.

## "Insulin delivery monitors" -> benefit (confidence=high)
- 'Insulin delivery monitors' names a specific, nameable device/item, appearing in a bulleted list of diagnostic supplies and devices alongside glucometers and continuous glucose monitors. A member could point to it and ask if it's covered.

## "Insulin delivery reservoirs" -> benefit (confidence=high)
- 'Insulin delivery reservoirs' is a specific, nameable diabetic supply item, listed alongside other concrete items like test strips, lancets, and glucose monitor sensors. A member could point to it and ask if it's covered.

## "Insulin pumps" -> benefit (confidence=high)
- Insulin pumps is a specific, nameable medical device/item that a member could ask about coverage for, appearing in a list of diabetes management equipment. It is a concrete covered item, not a generic category or fragment.

## "Intermediate vision lenses" -> benefit (confidence=high)
- 'Intermediate vision lenses' is a specific, nameable eyewear item listed as a covered lens option under the Lenses section. A member could point to it and ask whether it's covered, making it a real benefit.

## "Intradermal, scratch and puncture tests" -> benefit (confidence=high)
- The name refers to specific, nameable allergy testing procedures (intradermal, scratch, and puncture tests) under the Allergy Testing and Therapy section. A member could clearly point to these and ask if they're covered.

## "Known reaction to analgesics, anesthetics, etc." -> fragment_or_criterion (confidence=high)
- The name describes a medical condition/qualifier scenario (a patient having a known reaction to certain drugs), not a specific covered service or item. It reads as an eligibility criterion likely used to justify dental services in a hospital setting, so it is a fragment/criterion rather than a nameable benefit.

## "Laboratory examinations" -> benefit (confidence=high)
- 'Laboratory examinations' names a specific, identifiable diagnostic service that a member could ask about being covered. It appears in diagnostic/preventive and skilled nursing service lists as a concrete service, not a generic category word or a fragment/criterion.

## "Laboratory services" -> benefit (confidence=high)
- Laboratory services is a specific, nameable medical service that a member could ask about coverage for. It appears in a covered-services list under Behavioral Health. While somewhat broad, it names a concrete category of clinical service rather than an administrative/cost-share process word.

## "Laboratory tests related to the dialysis" -> benefit (confidence=high)
- 'Laboratory tests related to the dialysis' names a specific, identifiable service tied to dialysis treatment. A member could point to it and ask if lab tests during dialysis are covered. It is not a mere category word nor a fragment/criterion.

## "Lactation education and alternative fertility awareness counseling" -> benefit (confidence=high)
- The name refers to specific, nameable services: lactation education and fertility awareness counseling, appearing under Maternity Care. A member could point to it and ask if it's covered. It names concrete services rather than a generic category or a fragment/criterion.

## "Lamaze, parenting or other similar classes." -> benefit (confidence=medium)
- The name refers to specific, nameable services (Lamaze classes, parenting classes) that a member could ask about coverage for. Under Maternity Care, these are concrete educational offerings, not a generic category word or a fragment/criterion. The trailing 'or other similar classes' is a slight generalization but the core names specific services, so it qualifies as a benefit.

## "Lancets" -> benefit (confidence=high)
- Lancets are a specific, nameable medical item used in diabetes management. A member could point to it and ask if it's covered. It appears in a list of concrete supplies alongside test strips, syringes, and insulin.

## "Lens tolerance tests" -> benefit (confidence=high)
- 'Lens tolerance tests' is a specific, nameable diagnostic service within vision contact lens fitting, appearing alongside other specific tests like tear test, pupil evaluation, and cornea evaluation. A member could point to it and ask if it's covered.

## "Lenses may be molded or ground, glass or plastic." -> fragment_or_criterion (confidence=high)
- The name is a full sentence describing a characteristic/qualification of lenses ('may be molded or ground, glass or plastic') rather than naming a specific service or item. The actual benefit would be 'Lenses' (the section header); this extracted text is a descriptive sentence fragment, not a nameable benefit.

## "Lenticular aphakic" -> benefit (confidence=high)
- 'Lenticular aphakic' is a specific, nameable type of corrective lens appearing in a list of lens types (Myodisc, Aphakic, etc.). It names a concrete item a member could point to and ask if it's covered, independent of coverage status.

## "Lenticular aspheric aphakic" -> benefit (confidence=high)
- This names a specific type of corrective lens (a lenticular aspheric aphakic lens) - a concrete, nameable optical item a member could ask about. It appears in a list of specific lens types under Lenses. The fact it appears under 'We do not pay for' does not affect classification; it remains a real, specific item.

## "Lenticular aspheric myodisc" -> benefit (confidence=high)
- 'Lenticular aspheric myodisc' is a specific, nameable type of special lens listed among covered special lenses (Myodisc, Aphakic, etc.). A member could point to it and ask if it's covered. It is a concrete item, not a category word or fragment.

## "Lenticular myodisc" -> benefit (confidence=high)
- Lenticular myodisc is a specific, nameable type of special lens listed under 'We pay for the following special lenses.' It is a concrete item a member could ask about, not a generic category or fragment.

## "Licensed in the state of Michigan" -> fragment_or_criterion (confidence=high)
- The text 'Licensed in the state of Michigan' describes an eligibility/qualification criterion for the optometrist, not a specific nameable service. The excerpts show it as a condition ('The optometrist is: – Licensed in the state of Michigan'), which is clearly a criterion rather than a benefit.

## "Lid evaluation" -> benefit (confidence=high)
- Lid evaluation is a specific, nameable component of a contact lens fitting eye exam, appearing alongside other specific exam procedures like ophthalmoscopy and tear test. A member could point to it as a distinct service.

## "Life-threatening condition" -> fragment_or_criterion (confidence=medium)
- 'Life-threatening condition' under a Clinical Trials header describes an eligibility criterion/qualifying condition for coverage of routine patient costs, not a specific nameable service or item. It's a scenario/qualifier rather than a benefit.

## "Limitations and Exclusions" -> generic_administrative (confidence=high)
- This is a section heading describing a category of provisions (limitations and exclusions) rather than a specific, nameable covered service or item. It names a process/category, not a benefit.

## "Limited occlusal adjustments" -> benefit (confidence=high)
- 'Limited occlusal adjustments' names a specific dental procedure (adjusting the bite/occlusion) listed among other concrete basic dental services. It's a nameable service a member could ask about.

## "Living donor transplants not listed in this certificate" -> fragment_or_criterion (confidence=high)
- The name 'Living donor transplants not listed in this certificate' contains the qualifier 'not listed in this certificate,' which describes a scenario/exclusion criterion rather than naming a specific transplant service. While 'living donor transplants' alone might be a benefit category, the appended condition makes this a criterion describing which services fall outside coverage, not a nameable specific service a member could point to.

## "Localized delivery of antimicrobial agents" -> benefit (confidence=high)
- This names a specific, nameable dental periodontal service (localized delivery of antimicrobial agents) that a member could ask whether it's covered. It appears in a bulleted list of specific procedures alongside osseous surgeries and soft tissue grafts.

## "Loss of the device" -> fragment_or_criterion (confidence=high)
- 'Loss of the device' is not a nameable service or item; it describes a scenario/condition (a reason for device replacement) alongside similar items like 'Damage to the device so that it cannot be restored'. It's a criterion, not a benefit.

## "Magnetic resonance imaging (MRI)" -> benefit (confidence=high)
- MRI is a specific, nameable diagnostic imaging service under Radiology Services that a member could ask about coverage for.

## "Major restorative services" -> benefit (confidence=high)
- 'Major restorative services' names a specific, nameable dental service category (repair of decayed or damaged teeth, including onlays and crowns). It refers to concrete covered procedures a member could ask about, not a generic cost-share/process word or a fragment.

## "Marijuana (cannabis); medical or otherwise" -> benefit (confidence=medium)
- The name refers to a specific, nameable item (marijuana/cannabis, medical or otherwise) that a member could point to and ask about coverage. Under the Prescription Drugs header, it's a concrete item even though it's likely excluded. Exclusion status doesn't affect classification.

## "Marital counseling" -> benefit (confidence=high)
- 'Marital counseling' names a specific, nameable service a member could ask about. It appears in exclusion lists here, but coverage status must not drive classification. This is a real service type, not a generic category or fragment.

## "Meals, including special diets" -> benefit (confidence=medium)
- 'Meals, including special diets' names a specific, identifiable item/service provided during a hospital stay that a member could ask about. It's not a generic category word nor a fragment/criterion. Under 'Hospital Services' this refers to a concrete provision, so it qualifies as a benefit.

## "Medical supplies required for the use of an insulin pump" -> benefit (confidence=high)
- This names a specific, identifiable item -- medical supplies for an insulin pump -- appearing in a list of specific diabetes management items (test strips, lancets, syringes, insulin). A member could point to it and ask if it's covered. It's a real, nameable item, not a generic category or a condition/fragment.

## "Medical-Surgical Treatment" -> generic_administrative (confidence=low)
- The name 'Medical-Surgical Treatment' is a broad category term rather than a specific, nameable service. It describes a general kind of care rather than a particular procedure or item a member could point to. However, there are no direct excerpts and the header context (Contact Lenses) is confusing, so confidence is low.
- **Not auto-flagged**: below the high/medium-confidence precision gate.

## "Medically necessary and appropriate" -> fragment_or_criterion (confidence=high)
- This appears under 'Coverage Requirements' as a bullet describing a condition that autism services must meet ('must be medically necessary and appropriate'). It names no specific service; it's an eligibility criterion.

## "Medically necessary diagnostic services" -> benefit (confidence=medium)
- 'Medically necessary diagnostic services' names a specific category of service in the infertility treatment context that a member could ask about. While somewhat general, it refers to a nameable service (diagnostic services for infertility) rather than a pure administrative category or a fragment/criterion. Leaning toward benefit given guidance to prefer it when uncertain.

## "Medically necessary genetic testing" -> benefit (confidence=high)
- 'Medically necessary genetic testing' names a specific, identifiable service a member could ask about. The 'medically necessary' qualifier is a common modifier on real benefit names, and genetic testing is a concrete nameable service, not a category noun or eligibility fragment.

## "Medically necessary mammography" -> benefit (confidence=high)
- 'Medically necessary mammography' names a specific, identifiable diagnostic radiology service. It appears alongside other concrete imaging services (MRI, PET scans, nuclear cardiac studies). The 'medically necessary' qualifier distinguishes it from routine screening but it still refers to a nameable service a member could ask about.

## "Medications" -> generic_administrative (confidence=medium)
- "Medications" is a broad category noun rather than a specific nameable service or item. The excerpts show it as 'Medications administered during any service except an eye exam' - a general category of drugs/substances rather than a particular covered service. While it appears in an exclusion context, that isn't driving the classification; the term itself is a generic category word akin to 'Drugs'.

## "Member education and home programs" -> benefit (confidence=medium)
- 'Member education and home programs' names a specific, identifiable service offered in the context of therapy programs. It appears consistently as a bulleted item alongside other named services like 'Recreational therapy' and 'Sports medicine.' While somewhat broad, it refers to a nameable service a member could ask about, so it leans toward benefit.

## "Minor restorative services" -> benefit (confidence=high)
- 'Minor restorative services' is a specific, nameable category of dental services (repair of decayed or damaged teeth, including amalgam and resin restorations) that a member could point to and ask if covered. It's a recognized dental benefit class, not a generic cost-share/process word or a fragment/criterion.

## "Monitoring of ovarian response to ovulatory stimulants" -> benefit (confidence=high)
- This names a specific, identifiable medical service related to infertility treatment. It appears alongside other clearly specific services (artificial insemination, in vitro fertilization, ovarian wedge resection). A member could point to it and ask if it's covered, making it a real benefit regardless of coverage status.

## "Monthly (six-month supply)" -> fragment_or_criterion (confidence=medium)
- The name 'Monthly (six-month supply)' does not name a specific service or item. It appears under 'Contact Lenses' and describes a supply quantity/frequency qualifier for contact lenses rather than a distinct nameable benefit itself. It is a specification of a dispensing schedule, not a service.

## "Morbid Obesity Weight Management" -> benefit (confidence=high)
- 'Morbid Obesity Weight Management' names a specific, coverable service with defined visit limits (26 visits per member per year for BMI 30+). A member could ask 'is this covered?' It is not a generic category word nor a fragment/criterion.

## "Multiple extractions or removal of unerupted teeth" -> benefit (confidence=high)
- This names a specific, nameable dental service -- the extraction/removal of unerupted teeth. A member could ask whether this procedure is covered. It appears in a bulleted list of specific dental procedures alongside 'Alveoloplasty' and 'Diagnostic X-rays', confirming it is a concrete service rather than a category or criterion.

## "Myodisc" -> benefit (confidence=high)
- Myodisc is a specific, nameable type of special lens (used for high myopia). It appears under 'Lenses' as a distinct item in a list of covered special lenses, making it a concrete service/item a member could ask about.

## "Nerve conduction" -> benefit (confidence=high)
- Nerve conduction (study) is a specific, nameable diagnostic test, listed alongside EMG under Diagnostic Services. A member could point to it and ask if it's covered.

## "Newborn examination" -> benefit (confidence=high)
- 'Newborn examination' names a specific, identifiable medical service (an exam of a newborn given by a physician). A member could ask whether it's covered. It appears as a distinct bulleted benefit under Newborn Care.

## "No other means of transportation are available" -> fragment_or_criterion (confidence=high)
- The phrase 'No other means of transportation are available' is an eligibility requirement/condition for air ambulance coverage, not a specific nameable service. The excerpts show it as a bulleted requirement under 'Air ambulance services must also meet these requirements.'

## "Non-emergent air ambulance services between covered destinations" -> benefit (confidence=high)
- This names a specific, identifiable service -- non-emergent air ambulance transport between covered destinations. A member could point to it and ask whether it's covered. It appears under 'Ambulance Services' and describes a concrete service type, not a category noun or eligibility fragment.

## "Non-self-administered injectable drugs (except for select immunization vaccines)" -> benefit (confidence=high)
- The name refers to a specific, nameable category of items -- non-self-administered injectable drugs -- with a defined exclusion parenthetical. Under a Prescription Drugs header, a member could point to this and ask whether their injectable drug is covered. It names a specific type of service/item, not merely a generic administrative process word.

## "Non-surgical endodontic services" -> benefit (confidence=high)
- 'Non-surgical endodontic services' names a specific, nameable dental service (root canal therapy and related non-surgical endodontic treatment) that a member could ask about. It appears under 'Class II – Basic Services', a benefit category. This is a real benefit.

## "Non-surgical periodontic services" -> benefit (confidence=high)
- 'Non-surgical periodontic services' names a specific, identifiable category of dental services (treatment of gum disease without surgery) that a member could point to and ask about coverage. It appears under Class II Basic Services in dental plans, consistent with a real covered benefit.

## "Nonexperimental drugs to control blood sugar" -> benefit (confidence=high)
- This names a specific, identifiable item/service -- pharmaceutical drugs used to control blood sugar (excluding experimental ones). It appears in a list of concrete covered diabetes supplies (syringes, insulin, insulin pump supplies), and a member could clearly ask 'are my blood sugar control drugs covered?' The 'nonexperimental' qualifier is part of the specific service description, not a standalone eligibility fragment.

## "Not listed in this certificate or" -> fragment_or_criterion (confidence=high)
- The text 'Not listed in this certificate or' is a sentence fragment describing an exclusion condition, not a specific nameable service. It appears as a bullet qualifier in an exclusion list describing which services are not covered.

## "Not required to be covered under PPACA" -> fragment_or_criterion (confidence=high)
- The phrase 'Not required to be covered under PPACA' is a qualifier/condition describing which services are excluded, not a specific nameable service. It appears as a bullet in an exclusion criterion ('services that are: not listed... or not required to be covered under PPACA'). It names no service itself.

## "Nuclear cardiac studies" -> benefit (confidence=high)
- Nuclear cardiac studies is a specific, nameable diagnostic imaging service listed alongside other concrete tests like EKG, EEG, PET scans, and mammography. A member could point to it and ask if it's covered.

## "Nursing services" -> benefit (confidence=medium)
- 'Nursing services' names a specific, identifiable service that a member could ask about coverage for. While somewhat broad, it refers to a concrete category of care (nursing) rather than a generic administrative/cost-share word or a fragment/criterion. It appears alongside other clear benefit items like 'Semiprivate room' and 'Meals.' Leaning toward benefit per the guidance.

## "Nutritional therapy" -> benefit (confidence=high)
- 'Nutritional therapy' names a specific, nameable service that a member could ask about coverage for. It appears in a bulleted list of distinct covered services under Autism Spectrum Disorders alongside other clear benefits like genetic testing and outpatient mental health therapy.

## "Obstetrics" -> benefit (confidence=high)
- Obstetrics is a specific, nameable medical service area (maternity/childbirth care provided by a physician or certified nurse midwife). Members can point to it and ask if it's covered. It refers to concrete covered services, not a generic administrative category or a fragment.

## "Occlusal biteguards" -> benefit (confidence=high)
- An occlusal biteguard is a specific, nameable dental appliance/item that a member could ask about coverage for. It appears in a list of basic dental services.

## "Occupational therapy, Page 73" -> benefit (confidence=high)
- Occupational therapy is a real, specific, nameable service. The 'Page 73' suffix is an index/page reference artifact, but the core name refers to a genuine benefit.

## "Office visits after regularly scheduled hours" -> benefit (confidence=high)
- This names a specific, nameable dental service -- office visits occurring after regularly scheduled hours. A member could point to it and ask if it's covered. It appears as a distinct line item alongside other specific services like consultations and house/hospital calls.

## "Office visits for observation (during regularly scheduled hours)" -> benefit (confidence=medium)
- The name refers to a specific, nameable dental service - office visits for observation during regularly scheduled hours - appearing under a Basic Services class. A member could point to it and ask if it's covered. While it includes a timing qualifier, the core names a real service.

## "One exam per member, per calendar year" -> fragment_or_criterion (confidence=high)
- The name 'One exam per member, per calendar year' describes a frequency limitation/quantity rule, not a specific nameable service. It states how often something is covered rather than naming the service itself, making it a criterion/limitation fragment.

## "One eye exam every 12 months" -> benefit (confidence=high)
- Although phrased with a frequency limit, this names a specific, nameable service (an eye exam) that a member could ask about. The core service is an eye exam; the '12 months' qualifier describes its frequency but the name clearly refers to a real vision benefit.

## "One eye exam every calendar year" -> fragment_or_criterion (confidence=medium)
- The name describes a frequency limitation ('one eye exam every calendar year') rather than naming a specific service cleanly. The section header is 'Frequency' and the phrasing centers on the allowed quantity/interval. While it references an eye exam, the extracted name is really a frequency criterion. The underlying service (eye exam) is a benefit, but this particular candidate as extracted is a frequency rule.

## "One pair of frames every 12 months" -> fragment_or_criterion (confidence=medium)
- The name 'One pair of frames every 12 months' describes a frequency/quantity limitation under a 'Frequency' header, not a nameable service itself. The actual benefit is 'frames'; this phrasing is a frequency criterion. While frames are a real benefit, this specific extracted text expresses a frequency rule rather than naming the service.

## "One pair of frames every calendar year" -> benefit (confidence=medium)
- The name 'One pair of frames every calendar year' refers to a specific, nameable item (eyeglass frames) with a frequency limit. While it's phrased with frequency language, the core references frames -- a concrete vision benefit item a member could ask about. The 'every calendar year' portion is a frequency qualifier attached to a real item, not a standalone criterion.

## "One pair of lenses every 12 months" -> fragment_or_criterion (confidence=medium)
- The name 'One pair of lenses every 12 months' embeds a frequency limitation rather than naming a service cleanly. The underlying service ('lenses') is a real benefit, but this candidate is a frequency-clause phrasing extracted under the 'Frequency' header. It reads as a quantity/frequency rule rather than a clean nameable service. Leaning fragment_or_criterion but with medium confidence since 'lenses' is a real item embedded within.

## "One pair of lenses or contact lenses every 12 months" -> benefit (confidence=high)
- The name refers to a specific, nameable vision item (lenses or contact lenses), even though it includes a frequency qualifier. A member could point to this and ask if it's covered. The frequency limit ('every 12 months') is a benefit specification, not a mere fragment or generic category.

## "One pair of lenses or contact lenses every calendar year" -> benefit (confidence=medium)
- The name references a specific, nameable covered item (lenses or contact lenses), though phrased with a frequency limitation. The core service/item is real and identifiable, so it leans benefit despite the frequency qualifier.

## "One per member, per calendar year" -> fragment_or_criterion (confidence=high)
- The name 'One per member, per calendar year' describes a frequency limitation or coverage condition, not a specific nameable service. It answers 'how often' rather than 'what service,' making it a criterion/limitation fragment.

## "Only covered in an inpatient or outpatient hospital location" -> fragment_or_criterion (confidence=high)
- The text 'Only covered in an inpatient or outpatient hospital location' is a coverage condition/qualifier for ECT, not a specific nameable service. It's a sub-bullet describing where the actual benefit (Electroconvulsive Therapy) is covered.

## "Operating room services, including delivery and surgical treatment rooms" -> benefit (confidence=high)
- This names a specific, coverable service -- operating room services including delivery and surgical treatment rooms. A member could point to it and ask if it's covered. It appears under the 'Surgery' header and describes a concrete facility service, not a generic category word or a fragment/criterion.

## "Ophthalmoscopic examinations" -> benefit (confidence=high)
- Ophthalmoscopic examinations is a specific, nameable diagnostic procedure (examination of the eye's interior with an ophthalmoscope). It appears alongside other specific eye exam components like tonometry and visual acuity testing. A member could point to it and ask if it's covered.

## "Ophthalmoscopy" -> benefit (confidence=high)
- Ophthalmoscopy is a specific, nameable clinical procedure (examination of the eye's interior) that a member could point to and ask if it's covered. It appears as a distinct diagnostic evaluation within the contact lens exam list, not a generic category or fragment.

## "Oral brush biopsy sample collection" -> benefit (confidence=high)
- This names a specific, identifiable dental diagnostic procedure (collecting a sample via oral brush biopsy to identify cancerous/precancerous cells). A member could point to it and ask if it's covered. It is not a generic category word or a fragment/criterion.

## "Oral examinations/evaluations" -> benefit (confidence=high)
- Oral examinations/evaluations is a specific, nameable dental service found under diagnostic/preventive services. A member could clearly ask whether this is covered.

## "Oral surgery services" -> benefit (confidence=high)
- Oral surgery services names a specific, nameable category of dental services appearing under Class III Major Services. A member could point to it and ask if it's covered. It's a real dental benefit, not a generic administrative term or fragment.

## "Osseous surgeries" -> benefit (confidence=high)
- Osseous surgeries is a specific, nameable dental periodontal procedure appearing among a list of concrete services like gingivectomies, soft tissue grafts, and bone replacement grafts. A member could ask whether it is covered.

## "Osteopathic manipulation therapy (OMT) on any location of the body" -> benefit (confidence=high)
- This names a specific, nameable medical service -- osteopathic manipulative therapy (OMT) -- appearing under a relevant clinical header. The trailing qualifier 'on any location of the body' describes scope but the core is a real, pointable service a member could ask about.

## "Ostomy sets and accessories" -> benefit (confidence=high)
- Ostomy sets and accessories is a specific, nameable medical supply item a member could ask about coverage for. It appears in a bulleted list of concrete medical supplies alongside catheterization equipment and dressings.

## "Ostomy sets and accessories, catheterization equipment and urinary sets" -> benefit (confidence=high)
- The name lists specific, nameable medical items -- ostomy sets and accessories, catheterization equipment, and urinary sets -- which are concrete supplies a member could ask about. Under the 'Medical Supplies' header, these are real covered items despite being a compound list.

## "Other Dental Services" -> generic_administrative (confidence=high)
- "Other Dental Services" is a category/catch-all heading, not a specific nameable service. The actual specific services (e.g. TMJ treatment) are listed as sub-items beneath it. The name itself is a generic grouping label.

## "Other Services" -> generic_administrative (confidence=high)
- "Other Services" is a generic catch-all category label, not a specific nameable service. It appears as a bullet heading under Anesthesiology Services covering miscellaneous items, and does not itself name any particular covered service.

## "Other diagnostic and preventive services:" -> generic_administrative (confidence=high)
- This is a category header ('Other diagnostic and preventive services:') that groups specific sub-services beneath it (diagnostic tests, dental sealants, space maintainers). It describes a kind/grouping of provisions rather than naming a single specific service, and ends with a colon indicating it introduces a list.

## "Other medically necessary services related to dialysis treatment" -> generic_administrative (confidence=medium)
- The phrase 'Other medically necessary services related to dialysis treatment' is a catch-all category term rather than a specific nameable service. It uses the generic 'Other ... services' construction which describes a kind/category of provision rather than a particular service a member could point to. It appears in a bulleted list alongside generic items like 'Equipment', 'Drugs', 'Supplies'.

## "Outpatient Hospital Services:" -> generic_administrative (confidence=high)
- 'Outpatient Hospital Services' is a broad category/setting descriptor rather than a specific nameable service. It functions as a header grouping services delivered in an outpatient hospital setting, not a discrete benefit a member would point to and ask if covered.

## "Outpatient Psychiatric Care Facility and Office Setting" -> generic_administrative (confidence=medium)
- This is a setting/category header ('Outpatient Psychiatric Care Facility and Office Setting') that introduces a list of covered services provided in that setting, rather than naming a specific service itself. It describes the place/context of care, not a nameable service a member would ask 'is this covered?' The excerpts show it functioning as a subsection heading followed by 'We pay for the following services in a participating outpatient psychiatric care...'.

## "Outpatient Psychiatric Care Facility, Office Setting, Online and Virtual" -> benefit (confidence=medium)
- The name refers to outpatient psychiatric care delivered across specific settings (facility, office, online/virtual). Under the Behavioral Health Services header, this names a specific, coverable service a member could ask about. The 'settings' portion is descriptive of where the service is provided but the core is a real, nameable service (outpatient psychiatric care).

## "Outpatient mental health" -> benefit (confidence=medium)
- 'Outpatient mental health' names a specific, identifiable service (mental health care delivered in an outpatient setting) that a member could point to and ask about. While somewhat category-like, it refers to a concrete service type appearing in a bulleted benefit list, so it leans toward benefit.

## "Outpatient mental health therapy" -> benefit (confidence=high)
- Outpatient mental health therapy is a specific, nameable service that a member could ask about coverage for. It appears in a bulleted list alongside other clear benefits like nutritional therapy and genetic testing under autism spectrum disorders coverage.

## "Ovarian transposition" -> benefit (confidence=high)
- Ovarian transposition is a specific, nameable surgical procedure used in fertility preservation. It appears as a distinct bulleted service under the Fertility Preservation section, making it a real benefit a member could ask about.

## "Ovarian wedge resection or ovarian drilling" -> benefit (confidence=high)
- Ovarian wedge resection and ovarian drilling are specific, nameable surgical procedures used in infertility treatment. A member could point to this and ask if it's covered. It is a real medical service, not a generic category or fragment.

## "Oxygen and other gas therapy" -> benefit (confidence=high)
- 'Oxygen and other gas therapy' names a specific, identifiable medical service/item that a member could point to and ask if it's covered. It appears in a list of specific covered services within Skilled Nursing Facility Services. It is not a generic category word nor a fragment/criterion.

## "Oxygen and other therapeutic gases" -> benefit (confidence=high)
- 'Oxygen and other therapeutic gases' names a specific, identifiable item/supply that a member could point to and ask about coverage. It appears in a bulleted list of covered surgical items alongside other concrete services. It is a nameable therapeutic item, not a generic category word or a fragment/criterion.

## "Oxygen and other therapeutic gases and their administration" -> benefit (confidence=high)
- Names a specific, identifiable service/item -- oxygen and therapeutic gases plus their administration. A member could point to it and ask if it's covered. It appears in a list alongside other specific services like inhalation therapy and ECT, confirming it's a nameable benefit rather than a generic category or fragment.

## "Panniculectomy" -> benefit (confidence=high)
- Panniculectomy is a specific, nameable surgical procedure (removal of excess abdominal skin/tissue). It appears in a list of specific surgeries. Whether covered or excluded is irrelevant; it names a real service.

## "Parenting or other similar classes" -> benefit (confidence=medium)
- 'Parenting or other similar classes' names a specific, identifiable service (educational classes) that a member could ask about, even though it appears in an exclusion list. The 'or other similar classes' phrasing is a bit broad, but it still refers to a nameable service type rather than a category word or eligibility criterion. Coverage status (excluded) does not affect classification.

## "Part of a comprehensive rehabilitation plan" -> fragment_or_criterion (confidence=high)
- The text 'Part of a comprehensive rehabilitation plan' is a condition/qualifier in a bulleted list of criteria for when treatment to improve cognition may be paid for ('We may pay for treatment to improve cognition if it is: – Part of a comprehensive rehabilitation plan – Medically necessary...'). It does not name a specific service; it describes an eligibility criterion.

## "Part of a comprehensive rehabilitation plan, and" -> fragment_or_criterion (confidence=high)
- The name is a sentence fragment describing a condition/qualifier ('Part of a comprehensive rehabilitation plan, and') rather than naming any specific service. It reads as an eligibility criterion attached to Physical Therapy coverage, not a nameable benefit.

## "Participating facilities" -> fragment_or_criterion (confidence=high)
- 'Participating facilities' is a type of provider, not a specific covered service. It appears in a list of provider types (hospitals, physicians, nurse practitioners) describing who delivers chronic disease management services, not a nameable benefit a member would ask about.

## "Participating hospitals" -> fragment_or_criterion (confidence=high)
- 'Participating hospitals' appears as a provider type in a list describing who provides chronic disease management services, not as a nameable covered service or item. It describes the provider of care, not a benefit itself.

## "Patch and photo tests" -> benefit (confidence=high)
- Patch and photo tests are specific, nameable allergy diagnostic tests that a member could point to and ask if they're covered. They appear alongside other specific test types like intradermal, scratch and puncture tests under Allergy Testing and Therapy.

## "Patient is allergic to local anesthesia" -> fragment_or_criterion (confidence=high)
- This is a condition/eligibility criterion describing when general anesthesia may be justified, not a nameable service. The surrounding bullets ('Patient is medically impaired', 'Patient is younger than age seven') confirm these are qualifying scenarios, not benefits.

## "Patient is medically impaired or compromised" -> fragment_or_criterion (confidence=high)
- The name describes a patient condition/eligibility scenario (part of a list of criteria for when general anesthesia might be covered), not a specific nameable service. Surrounding bullets are similar criteria ('Patient is allergic to local anesthesia', 'Patient is younger than age seven').

## "Patient is younger than age seven" -> fragment_or_criterion (confidence=high)
- This is an eligibility condition describing when general anesthesia/IV sedation is justified, not a nameable service. It appears in a list of criteria (medically impaired, allergic to anesthesia) that qualify coverage, so it names no specific service.

## "Periodontal scaling and root planing" -> benefit (confidence=high)
- This names a specific, well-known dental procedure (periodontal scaling and root planing) that a member could ask about. It appears in a list of specific services under major dental services, making it a clear benefit.

## "Peripheral blood stem cell (including peripheral blood stem cell pheresis)" -> benefit (confidence=high)
- The name refers to a specific, nameable medical service/procedure -- peripheral blood stem cell collection including pheresis. This is a concrete clinical service a member could ask about, appearing under an Oncology Clinical Trials header, clearly a real benefit rather than a generic category or fragment.

## "Photochromatic glass lenses" -> benefit (confidence=high)
- This names a specific, nameable eyewear item (photochromatic glass lenses) appearing in a list of specific lens types under a 'Lenses' section. A member could point to it and ask if it's covered, regardless of coverage status.

## "Photochromatic lenses" -> benefit (confidence=high)
- Photochromatic lenses is a specific, nameable vision item that a member could ask about coverage for. It appears in a list of lens options alongside other specific items like progressive lenses and anti-reflective lenses. This is a real benefit item, not a generic category or fragment.

## "Physical therapists" -> benefit (confidence=medium)
- 'Physical therapists' names a specific type of provider whose services are covered. It appears in a list of provider types. While it's a provider rather than a service, it refers to a specific, nameable category a member could ask about (physical therapy services). It's specific rather than a generic administrative process word or a fragment. Leaning toward benefit per guidance.

## "Physical therapy (see Page 86 for physical therapy services)" -> benefit (confidence=high)
- The core name 'Physical therapy' is a real, specific, nameable covered service. The parenthetical cross-reference ('see Page X for physical therapy services') is just a pointer artifact and doesn't change that the name refers to a legitimate benefit a member could ask about.

## "Physical therapy (see Page 91 for physical therapy services)" -> benefit (confidence=medium)
- The core name 'Physical therapy' refers to a specific, nameable service a member could ask about. The parenthetical cross-reference ('see Page 91 for physical therapy services') is just a pointer artifact, not part of the benefit itself. Despite appearing under 'Dental Services' header, the underlying service is a real benefit.

## "Physical therapy or (see Page 83 for physical therapy services)" -> fragment_or_criterion (confidence=medium)
- While 'Physical therapy' is a real benefit, the extracted name is actually a cross-reference fragment ('Physical therapy or (see Page 83 for physical therapy services)') rather than a clean benefit name. The trailing 'or' and parenthetical pointer indicate this is a mis-extracted sentence fragment/navigational reference rather than a proper benefit name entry.

## "Physical therapy, Page 86" -> benefit (confidence=medium)
- The core name 'Physical therapy' is a real, specific, nameable service that a member could ask about. The 'Page 86' suffix appears to be an index/table-of-contents artifact rather than part of the benefit name. Despite the extraction noise, the underlying service is a genuine benefit.

## "Physical therapy, Page 91" -> benefit (confidence=high)
- Physical therapy is a specific, nameable covered service under Home Health Care Services. Despite the appended page reference, the name refers to a concrete therapy service a member could ask about.

## "Physician services (up to two visits per week)" -> benefit (confidence=high)
- 'Physician services' is a specific, nameable service that a member could ask about coverage for. The parenthetical '(up to two visits per week)' is a frequency limitation on that benefit, not a disqualifier. In the context of Skilled Nursing Facility Services, this names a real covered service.

## "Physician services are payable for tests such as:" -> fragment_or_criterion (confidence=high)
- This is a sentence lead-in phrase ('Physician services are payable for tests such as:') that introduces a list of actual tests. It does not name a specific service itself; the real benefits are the listed items (Thyroid function, EKG, EEG, etc.). The phrase is a fragment/introductory clause, not a nameable service.

## "Physician services by a member of the hospice interdisciplinary team" -> benefit (confidence=high)
- This names a specific, nameable service -- physician services provided by a member of the hospice interdisciplinary team. It appears as a distinct bulleted item under Hospice Care Services alongside other clearly nameable services like nursing care and respite care. A member could point to this and ask whether it's covered.

## "Physician services not paid by the hospital" -> fragment_or_criterion (confidence=medium)
- The name describes a payment scenario/qualifier ('not paid by the hospital') rather than a specific nameable service. 'Physician services' is itself a broad category, and the qualifier makes this a condition about billing rather than a distinct covered service a member could point to.

## "Physician's surgical fee" -> benefit (confidence=medium)
- 'Physician's surgical fee' names a specific, identifiable service/charge—the fee for a physician performing surgery—that a member could ask about. Under the 'Surgery' header this refers to a concrete covered item. While it names a fee, it's tied to a specific nameable service rather than being a generic cost-share category like 'Coinsurance'.

## "Physicians" -> fragment_or_criterion (confidence=high)
- 'Physicians' appears in a list of provider types who provide chronic disease management services, not as a named service or item. It describes who delivers care (a provider category/qualifier), not a specific coverable benefit a member could point to and ask 'is this covered?'

## "Physicians and Other Professional Providers" -> generic_administrative (confidence=high)
- This names a category of provider type rather than a specific, nameable covered service. It describes who may render services, not a particular service or item a member would point to and ask if it's covered.

## "Planning services" -> benefit (confidence=low)
- Under 'Infertility Treatment', 'Planning services' appears as a specific listed covered service alongside 'diagnostic services' and 'counseling services'. While somewhat generic-sounding, in this context it refers to a nameable service (infertility planning services) a member could ask about. Leaning toward benefit per guidance, but with low confidence given the vague wording.

## "Plastic photosensitive lenses (Transitions®)" -> benefit (confidence=high)
- This names a specific, nameable item -- photosensitive plastic lenses (Transitions brand) -- a concrete product a member could ask about coverage for under a vision plan's Lenses section.

## "Polarized lenses" -> benefit (confidence=high)
- 'Polarized lenses' is a specific, nameable vision care item that a member could ask about being covered. It appears under the 'Lenses' section alongside other specific lens types like photochromatic and plastic photosensitive lenses.

## "Polycarbonate lenses" -> benefit (confidence=high)
- Polycarbonate lenses is a specific, nameable vision item that a member could ask about coverage for. It appears under the Lenses section as a distinct lens type, making it a real benefit.

## "Polycarbonate lenses for children through 18 years of age" -> benefit (confidence=high)
- This names a specific, nameable item (polycarbonate lenses) covered under the Lenses section, with an age qualifier. A member could point to it and ask if it's covered. It's a real vision benefit item, not a generic category or fragment.

## "Porcelain, ceramic and cast metal retainers for resin-bonded bridges" -> benefit (confidence=high)
- This names a specific, nameable dental item -- porcelain, ceramic and cast metal retainers used for resin-bonded bridges, a Class III major dental service. A member could point to it and ask if it's covered.

## "Positron emission tomography (PET) scans" -> benefit (confidence=high)
- PET scans are a specific, nameable diagnostic imaging service appearing under Radiology Services. A member could clearly ask whether this is covered.

## "Post-coital test" -> benefit (confidence=high)
- A post-coital test is a specific, nameable diagnostic procedure used in infertility evaluation. A member could point to it and ask whether it's covered, so it qualifies as a real benefit regardless of coverage status.

## "Post-menopausal members" -> fragment_or_criterion (confidence=high)
- The name 'Post-menopausal members' does not name a specific service or item; it describes a category/population of members, likely used as an eligibility or exclusion criterion under the Fertility Preservation section. It is not something a member points to and asks 'is this covered?' as a service.

## "Preauthorization" -> generic_administrative (confidence=high)
- Preauthorization is a process/administrative term describing a requirement to obtain approval before receiving services, not a specific nameable service or item. It appears under Prescription Drugs but describes a process rather than a covered benefit.

## "Prescription drugs including hormone therapy (see Prescription Drugs)" -> benefit (confidence=medium)
- The name refers to prescription drugs including hormone therapy, which is a specific, nameable covered service (particularly under Gender Affirming Services). The 'see Prescription Drugs' is a cross-reference artifact but the core names real services. Leaning toward benefit.

## "Prescription drugs that are experimental or investigational." -> fragment_or_criterion (confidence=high)
- The name 'Prescription drugs that are experimental or investigational' does not name a specific, pointable service or item; it describes a qualifier/condition (experimental or investigational status) applied to prescription drugs. This is a criterion-based exclusion clause rather than a nameable benefit.

## "Prescription drugs that we consider to be cosmetic" -> fragment_or_criterion (confidence=medium)
- The name 'Prescription drugs that we consider to be cosmetic' does not name a specific, nameable service or item. It describes a category qualified by a subjective criterion ('that we consider to be cosmetic'), functioning as an exclusion clause rather than a pointable benefit. This is parallel to 'Prescription drugs that are experimental or investigational' which is also a qualifier-based exclusion. It's not a discrete service a member could point to.

## "Preventive drugs" -> benefit (confidence=medium)
- 'Preventive drugs' names a specific, identifiable category of medications covered under prescription drug benefits (a member could ask if their preventive drug is covered). While somewhat broad, it refers to a nameable class of covered items rather than a generic process/cost-share word or a fragment. It appears as a named benefit heading alongside Immunization Vaccines, Supplements and Vitamins.

## "Prior Authorization" -> generic_administrative (confidence=high)
- 'Prior Authorization' is an administrative process/requirement, not a specific nameable covered service. The excerpts confirm it refers to a coverage requirement ('Do not meet prior authorization requirements') rather than an item or service a member could point to and ask if it's covered.

## "Prior Authorization for Specialty Pharmaceuticals" -> generic_administrative (confidence=high)
- 'Prior Authorization for Specialty Pharmaceuticals' describes a process/administrative requirement (prior authorization) rather than naming a specific covered service or item. It's a category/process phrase, not a nameable benefit a member could ask 'is this covered?' about.

## "Private duty nursing" -> benefit (confidence=high)
- Private duty nursing is a specific, nameable healthcare service that a member could ask about coverage for. It appears in bulleted lists (here as an exclusion) but the name itself refers to a concrete service, so it qualifies as a benefit regardless of coverage status.

## "Procedures that are payable in the circumstances explained above include:" -> fragment_or_criterion (confidence=high)
- This is a sentence lead-in phrase ('Procedures that are payable in the circumstances explained above include:') that introduces a list rather than naming a specific service. It describes a condition/scenario, not a nameable benefit.

## "Progressive lenses" -> benefit (confidence=high)
- Progressive lenses is a specific, nameable vision item that a member could ask about coverage for. It appears under 'Lenses' as a distinct lens option, alongside other specific lens types.

## "Prophylaxes" -> benefit (confidence=high)
- Prophylaxes refers to dental cleanings, a specific, nameable preventive dental service listed alongside oral examinations and fluoride treatments. A member could point to it and ask if it's covered.

## "Prosthetics and orthotics" -> benefit (confidence=high)
- Prosthetics and orthotics are specific, nameable medical items/devices a member could ask about coverage for. Despite appearing in coinsurance/cost-share lists, the name itself refers to concrete covered items, not a generic category or fragment.

## "Prosthodontic services" -> benefit (confidence=high)
- Prosthodontic services is a specific, nameable category of dental services (repair or replace missing or deficient natural teeth or tissue). A member could ask 'is prosthodontic care covered?' It refers to a concrete class of dental services, not a generic cost-share or administrative process, and it is not a fragment or eligibility criterion.

## "Provided as part of a chemotherapy program and" -> fragment_or_criterion (confidence=high)
- The name 'Provided as part of a chemotherapy program and' is a sentence fragment describing a condition/criterion for coverage, not a specific nameable service. The excerpts show it's part of a bulleted list of qualifying conditions (approved by FDA, treatment of malignant disease, etc.) rather than a benefit name itself.

## "Provider’s equipment, such as stethoscopes" -> fragment_or_criterion (confidence=medium)
- The name 'Provider's equipment, such as stethoscopes' describes a category of items typically excluded from DME coverage (provider-owned tools), not a specific nameable benefit a member would request. It reads as an exclusion clause/example rather than a distinct covered service. However, some ambiguity exists since 'stethoscopes' is a nameable item, so medium confidence.

## "Psychiatric Intensive Outpatient Program (IOP)" -> benefit (confidence=high)
- Psychiatric Intensive Outpatient Program (IOP) is a specific, nameable level of behavioral health care that a member could ask whether it's covered. It is a distinct clinical service, not a generic category or fragment.

## "Psychiatric Partial Hospitalization Program (PHP)" -> benefit (confidence=high)
- Psychiatric Partial Hospitalization Program (PHP) is a specific, nameable level of behavioral health care that a member could point to and ask if it's covered. It names a concrete service, not a generic category or fragment.

## "Psychological testing" -> benefit (confidence=high)
- Psychological testing is a specific, nameable clinical service under Behavioral Health that a member could ask whether it's covered. It appears alongside other specific services like individual/group psychotherapeutic treatment and family counseling.

## "Psychological testing, evaluation, or therapy for allergies" -> benefit (confidence=medium)
- The name refers to a specific, nameable service -- psychological testing, evaluation, or therapy specifically for allergies. Under the 'Allergy Testing and Therapy' section, this is a concrete service a member could ask about (likely excluded, but exclusion status doesn't matter). It names a specific type of service, not a generic category or a fragment/criterion.

## "Psychologists" -> fragment_or_criterion (confidence=medium)
- 'Psychologists' is a type of provider/practitioner, not a specific nameable service or item. It appears in a list of provider types (clinical nurse specialists, social workers, physical therapists, etc.) rather than describing a covered service. A member wouldn't ask 'is Psychologists covered?' — provider types describe who renders care, not a benefit itself. It's closest to a non-service descriptor, though it could arguably be seen as a generic category.

## "Pulmonary function evaluation" -> benefit (confidence=high)
- Pulmonary function evaluation is a specific, nameable diagnostic service that a member could point to and ask if it's covered. It appears in a list alongside other specific services like Inhalation therapy and Electroconvulsive Treatment.

## "Pulmonary function studies" -> benefit (confidence=high)
- Pulmonary function studies is a specific, nameable diagnostic test that a member could ask whether it's covered. It appears alongside other specific diagnostic services like EKG and EEG under Diagnostic Services.

## "Pupil evaluation" -> benefit (confidence=high)
- 'Pupil evaluation' is a specific, nameable clinical vision service appearing in a list of concrete contact lens fitting evaluations (biomicroscopic, lid, cornea, etc.). A member could ask whether this specific evaluation is covered.

## "Qualified individual" -> fragment_or_criterion (confidence=high)
- 'Qualified individual' is an eligibility criterion/definition describing who may receive services, not a specific nameable service or item. The excerpts confirm it defines a member status ('must be a qualified individual according to the terms of this certificate') rather than naming a covered service.

## "Radioactive isotope studies and use of radium" -> benefit (confidence=high)
- This names specific, nameable radiology services (radioactive isotope studies and use of radium) listed alongside other concrete diagnostic services like X-rays, ultrasound, and CAT scans. A member could point to it and ask if it's covered.

## "Recementation of fixed bridges" -> benefit (confidence=high)
- This names a specific, nameable dental procedure (recementing fixed bridges) that a member could point to and ask if it's covered. It appears under Class II Basic Services as a distinct service item.

## "Recementation or repair of posts, crowns, veneers, inlays and onlays" -> benefit (confidence=high)
- This names a specific, nameable dental service (recementation or repair of posts, crowns, veneers, inlays and onlays) under Class II Basic Services. A member could point to this and ask if it's covered. Length does not disqualify it as a benefit.

## "Recovery room" -> benefit (confidence=high)
- 'Recovery room' names a specific, identifiable facility service associated with surgery that a member could point to and ask if it's covered. It appears in a benefit bullet list alongside other concrete services like anesthesia and nursing care.

## "Recreational therapy" -> benefit (confidence=high)
- Recreational therapy is a specific, nameable therapeutic service that a member could ask whether it's covered. It appears in lists alongside other named services. Its appearance in these excerpts (possibly as an exclusion) does not affect classification.

## "Refills of prescriptions for covered drugs that exceed BCBSM’s limits:" -> fragment_or_criterion (confidence=high)
- The name describes a scenario/limitation ('Refills...that exceed BCBSM's limits') rather than naming a specific covered service or item. It is a condition/limitation clause, not a nameable benefit.

## "Related reading and interpretation of your test results" -> benefit (confidence=medium)
- This names a specific, nameable service under Preventive Care Services -- the reading and interpretation of preventive test results by a provider. A member could point to it and ask whether it's covered. It's more specific than a generic category word and does describe an actual service rendered, so it leans toward benefit.

## "Removal of the equipment after it is no longer needed" -> fragment_or_criterion (confidence=high)
- The phrase 'Removal of the equipment after it is no longer needed' describes a scenario/condition within dialysis services rather than naming a specific, distinct covered service. It's a sub-clause elaborating on what's included in dialysis equipment provisions, not a nameable benefit a member would ask about independently.

## "Repairs of bridges" -> benefit (confidence=high)
- 'Repairs of bridges' is a specific, nameable dental service under Class III Major Services that a member could ask about coverage for. It refers to a concrete procedure, not a generic category or an eligibility fragment.

## "Repairs, limited to the cost of a new device" -> fragment_or_criterion (confidence=medium)
- The name describes a limitation/qualifier ('limited to the cost of a new device') rather than naming a specific service. While 'Repairs' of prosthetic/orthotic devices could be a nameable service, the phrasing here is a limitation clause describing a cost cap rather than a clean benefit name, leaning toward fragment/criterion.

## "Residential and Outpatient Substance Abuse Treatment Facility" -> benefit (confidence=high)
- The name refers to a specific, nameable service/facility -- residential and outpatient substance abuse treatment. A member could point to it and ask if it's covered. It appears as a distinct bulleted benefit under Behavioral Health Services with its own medical necessity criteria, indicating it names an actual covered service rather than a generic category or fragment.

## "Rh(D) incompatibility screening" -> benefit (confidence=high)
- Rh(D) incompatibility screening is a specific, nameable preventive service (a recognized prenatal screening test). It appears under Preventive Care Services and refers to a concrete diagnostic screening a member could ask about.

## "Rhinoplasty" -> benefit (confidence=high)
- Rhinoplasty is a specific, nameable surgical procedure. Though it appears in an exclusion context here, it names a concrete service, so it qualifies as a benefit regardless of coverage status.

## "Room and board" -> benefit (confidence=medium)
- "Room and board" refers to a specific, nameable service item in a residential treatment facility that a member could ask whether it is covered. While somewhat generic-sounding, it is a concrete facility service item listed as a covered component, not a process/cost-share category word like coinsurance or a fragment/criterion. Leaning toward benefit per guidance.

## "Routine Flexible Sigmoidoscopy Examination" -> benefit (confidence=high)
- This names a specific, nameable medical service (a routine flexible sigmoidoscopy examination) that a member could ask about coverage for. It appears under Preventive Care Services with specific frequency limits, confirming it is a concrete benefit.

## "Routine Gynecological Examination" -> benefit (confidence=high)
- Names a specific, nameable preventive service with defined coverage limits (two visits per member per calendar year). A member could point to it and ask if it's covered.

## "Routine Laboratory Services" -> benefit (confidence=high)
- 'Routine Laboratory Services' names a specific, identifiable preventive care service that a member could ask about coverage for. It appears under Preventive Care Services as a covered benefit with defined frequency limits. While somewhat categorical, it refers to a concrete, nameable service item.

## "Routine Pap Smear" -> benefit (confidence=high)
- 'Routine Pap Smear' is a specific, nameable medical screening service listed under Preventive Care Services with defined frequency limits. A member could clearly ask whether it's covered.

## "Routine care" -> benefit (confidence=medium)
- 'Routine care' under the Newborn Care section refers to a specific, nameable service—routine care during the newborn's eligible hospital stay. While somewhat broad, it names a concrete covered service a member could ask about, rather than a category/cost-share word or a fragment/criterion. Leaning toward benefit per guidance.

## "Routine care during the newborn’s eligible hospital stay." -> benefit (confidence=medium)
- The name refers to a specific, nameable service -- routine care provided to a newborn during their hospital stay -- which a member could point to and ask if it's covered. It appears under Maternity/Newborn Care headers. While it includes a qualifier ('during the newborn's eligible hospital stay'), the core is a specific covered service (routine newborn care), not merely a category word or a bare eligibility criterion.

## "Routine dental services" -> benefit (confidence=high)
- 'Routine dental services' names a specific, nameable category of care that a member could ask about being covered. Though it appears in exclusion lists here, coverage status is irrelevant. It refers to an identifiable service type (routine dental care), making it a benefit rather than a generic administrative word or a fragment/criterion.

## "Routine eye exams or services" -> benefit (confidence=high)
- 'Routine eye exams' is a specific, nameable service a member could ask about. Though it appears under exclusions, coverage status doesn't affect classification. It names a concrete service under Optometrist Services.

## "Routine laboratory tests" -> benefit (confidence=high)
- 'Routine laboratory tests' names a specific, identifiable medical service that a member could ask about being covered. It appears in a list of covered dialysis-related services and refers to an actual nameable service, unlike the generic 'Equipment' or 'Drugs' entries in the same list.

## "Routine maintenance of a prosthetic device" -> benefit (confidence=medium)
- The name refers to a specific, nameable service -- maintenance of a prosthetic device -- that a member could ask whether it is covered. It appears in exclusion lists here, but coverage status must not influence classification. It is not a generic category word nor a mere fragment/criterion; it names a concrete service.

## "Routine patient costs" -> benefit (confidence=medium)
- 'Routine patient costs' in the context of clinical trials is a specific, defined coverage category referring to the routine care items and services associated with participating in an approved clinical trial. It is a nameable benefit that members can ask whether it's covered, and appears as a distinct benefit heading under Clinical Trials. While the phrasing is somewhat generic-sounding, in insurance parlance it is a recognized specific benefit tied to clinical trial participation.

## "Screening Mammography" -> benefit (confidence=high)
- Screening mammography is a specific, nameable medical service to screen for breast cancer. It appears as a distinct bulleted benefit under Preventive Care Services with defined frequency limits.

## "Screening, counseling and prescription drugs to help you stop smoking" -> benefit (confidence=high)
- This names a specific set of covered preventive services (smoking cessation screening, counseling, and prescription drugs) that a member could point to and ask about. It appears under Preventive Care Services and describes a nameable, specific service rather than a generic category or eligibility criterion.

## "Search of an international donor registry" -> benefit (confidence=high)
- 'Search of an international donor registry' names a specific, identifiable service (searching a donor registry for matches), something a member could point to and ask if it's covered. It appears in an exclusion list here, but coverage status must not drive the classification. The name refers to a concrete nameable service, not a generic category or a fragment/criterion.

## "Select high abuse drugs" -> benefit (confidence=medium)
- 'Select high abuse drugs' names a specific category of drug items (drugs with high abuse potential) that a member could point to and ask about coverage. It appears alongside other real drug items like 'Compounded hormones' and 'Dietary supplements' in an exclusion list. While somewhat category-like, it refers to a specific nameable class of items rather than a process or eligibility rule. Its exclusion status does not affect classification.

## "Select immunization vaccines" -> benefit (confidence=high)
- 'Select immunization vaccines' names a specific, nameable covered item (immunization vaccines). A member could point to it and ask if it's covered. It is a specific service/item rather than a generic category word or a fragment/criterion.

## "Select services, equipment, and tools to manage hypertension" -> fragment_or_criterion (confidence=low)
- The name begins with 'Select services, equipment, and tools' which describes a generic bundle/category rather than a specific nameable service, though it references hypertension management under a condition management program. It's a vague grouping phrase rather than a single specific benefit. Leaning toward fragment/generic due to the non-specific 'select services, equipment, and tools' framing, but no excerpts available so confidence is low.
- **Not auto-flagged**: below the high/medium-confidence precision gate.

## "Select services, equipment, tools to manage Type 2 diabetes" -> benefit (confidence=low)
- The name refers to services, equipment, and tools to manage Type 2 diabetes under a condition management program. While it starts with 'Select services, equipment, tools' which leans generic/category-like, it is tied to a specific condition (Type 2 diabetes management) and names a specific offering under the ECMP. Given the guidance to lean toward 'benefit' when uncertain and the specific disease-management context, I classify it as a benefit but with low confidence due to the generic-sounding lead-in.

## "Self-administered, over-the-counter drugs" -> benefit (confidence=medium)
- The name refers to a specific, nameable category of items -- over-the-counter drugs that are self-administered. A member could point to this and ask whether it's covered. It names a real class of items rather than a process word or a fragment/criterion. While somewhat categorical, it's more specific than pure administrative terms like 'Drugs' alone, so leaning toward benefit.

## "Semiprivate room" -> benefit (confidence=high)
- A semiprivate room is a specific, nameable inpatient hospital accommodation that a member could ask about coverage for. It appears in a list of concrete hospital services (nursing, meals, etc.), and is a distinct covered item rather than a generic category or fragment.

## "Septorhinoplasty" -> benefit (confidence=high)
- Septorhinoplasty is a specific, nameable surgical procedure. Its appearance in an exclusion context does not affect classification; it names a concrete service a member could ask about.

## "Services by a nonparticipating ambulatory surgery facility" -> benefit (confidence=medium)
- The name refers to a specific, nameable service -- services provided by a nonparticipating ambulatory surgery facility. A member could point to this and ask if it's covered. While it appears under 'we do not pay for,' coverage status must not drive classification. It names a real service type distinguished by provider type, which is specific enough to be a benefit rather than a pure category word or a fragment.

## "Services covered under any other health plan" -> fragment_or_criterion (confidence=high)
- 'Services covered under any other health plan' does not name a specific service or item; it describes a condition/scenario (coordination of benefits / services already covered elsewhere) used as an exclusion criterion. It's a qualifier, not a nameable benefit.

## "Services not related to the dialysis process" -> fragment_or_criterion (confidence=high)
- The name 'Services not related to the dialysis process' does not name a specific, nameable service. It describes an exclusionary scenario/qualifier -- services that fall outside the dialysis process. It parallels the adjacent items like 'Services not provided by the employees of the ESRD facility,' which are also condition/scenario descriptions rather than specific benefits.

## "Services that are not BCBSM benefits" -> fragment_or_criterion (confidence=high)
- 'Services that are not BCBSM benefits' does not name any specific, nameable service or item. It is a self-referential qualifier/criterion describing a category of exclusion (anything not covered), not a concrete service a member could point to. This is a criterion, independent of its exclusion status.

## "Services that are not focused on improving the member’s functioning" -> fragment_or_criterion (confidence=high)
- The name is a descriptive clause characterizing a category of services by a qualifier ('that are not focused on improving the member's functioning') rather than naming a specific, nameable service. It reads as an exclusion criterion, not a benefit item.

## "Services to treat temporomandibular joint dysfunction (except as described above)" -> fragment_or_criterion (confidence=medium)
- While 'services to treat temporomandibular joint dysfunction' names a real service area, the actual candidate name is framed as an exclusion clause qualifier ('except as described above'), which points back to another provision rather than naming a specific coverable service. The core phrasing reads as a limitation/exclusion clause. However, there is a real service concept (TMJ treatment) embedded, so confidence is medium; the trailing qualifier makes this read more like a fragment/criterion than a clean benefit name.

## "Severe respiratory disease" -> fragment_or_criterion (confidence=high)
- This is a medical condition listed as an eligibility criterion (part of a list of conditions that qualify for something under Dental Services), not a specific covered service or item. It describes a patient condition, not a nameable benefit.

## "Sexually transmitted infection screening" -> benefit (confidence=high)
- This names a specific, nameable preventive care service - screening for sexually transmitted infections. It appears in a list alongside other clearly specific benefits like cervical cancer screening and HIV counseling and screening. A member could ask 'is this covered?'

## "Simple extractions" -> benefit (confidence=high)
- Simple extractions refers to a specific, nameable dental procedure (tooth extraction) that a member could ask whether it's covered. It appears under Class II Basic Services as a distinct covered dental service.

## "Six visits for children 13 months through 23 months" -> fragment_or_criterion (confidence=high)
- This is a visit-frequency limitation describing how many well-child visits are allowed for a specific age range, not a nameable service itself. It's a quantity/eligibility qualifier under the actual benefit (preventive/well-child care visits), so it describes a condition rather than naming a specific covered service.

## "Six visits for children 24 months through 35 months" -> fragment_or_criterion (confidence=medium)
- This is a visit-count/age-range specification ('Six visits for children 24 months through 35 months') describing the frequency limit for well-child visits, not a nameable service itself. The actual benefit is 'Well-child visits'; this candidate is a sub-detail describing quantity and eligibility age range, so it functions as a criterion/limitation fragment rather than a distinct benefit.

## "Skin" -> benefit (confidence=high)
- In context, 'Skin' refers to skin transplants (a specific, nameable transplant service alongside cornea and bone marrow transplants). This is a real, specific covered service under Transplant Services.

## "Sleep apnea treatments:" -> benefit (confidence=medium)
- 'Sleep apnea treatments' names a specific, identifiable category of medical service that a member could ask about coverage for. While it's somewhat broad, it refers to a concrete nameable clinical treatment area (with sub-items like rhinoplasty/septorhinoplasty listed under it), not an administrative cost-share word or a fragment/criterion. It appears in the Surgery section as a real service line.

## "Sleep studies and surgeries to diagnose and treat sleep apnea" -> benefit (confidence=high)
- Names a specific, nameable service -- sleep studies and surgeries to diagnose and treat sleep apnea -- that a member could ask about coverage for. Appears as a bulleted covered service under Surgery.

## "Soft tissue grafts" -> benefit (confidence=high)
- Soft tissue grafts is a specific, nameable dental periodontal procedure appearing alongside other specific services like gingivectomies and bone replacement grafts. A member could ask whether this is covered.

## "Solutions" -> generic_administrative (confidence=medium)
- "Solutions" is a generic category noun appearing in a list alongside similar generic items like "Equipment", "Drugs", "Supplies", and "Other medically necessary services". It does not name a specific, pointable service; it's a vague catch-all category for dialysis solutions rather than a discrete nameable benefit.

## "Space maintainers" -> benefit (confidence=high)
- Space maintainers are a specific, nameable dental device/service used to hold space for teeth. A member could ask 'is this covered?'. It appears under Basic Services as a distinct item.

## "Spare prosthesis devices" -> benefit (confidence=high)
- 'Spare prosthesis devices' names a specific, nameable item -- a backup/duplicate prosthetic device. A member could point to it and ask if it's covered. It appears in exclusion lists here, but exclusion status must not drive classification. It is a concrete item, not a generic category word or a condition/criterion fragment.

## "Special treatment rooms" -> benefit (confidence=medium)
- 'Special treatment rooms' names a specific, identifiable facility item/service within Skilled Nursing Facility Services, listed alongside other concrete covered items like laboratory examinations and oxygen therapy. It refers to a nameable thing a member could ask about, not a generic category or a criterion/fragment.

## "Specialty Pharmaceuticals" -> benefit (confidence=high)
- Specialty Pharmaceuticals refers to a specific, nameable category of drugs (specialty/specialty chemotherapy drugs) that a member could ask 'is this covered?' The excerpts describe payment for approved specialty drugs, making it a concrete covered item rather than a generic process word or a fragment.

## "Spectrum Disorders" -> fragment_or_criterion (confidence=medium)
- The candidate 'Spectrum Disorders' is a truncated fragment of 'Autism Spectrum Disorders'. On its own, 'Spectrum Disorders' does not name a specific service or condition benefit -- it's an incomplete phrase clipped from the full term. The excerpts consistently show it as part of 'Autism Spectrum Disorders', indicating this is an extraction artifact rather than a standalone nameable benefit.

## "Speech language therapy, Page 121" -> benefit (confidence=medium)
- The core name 'Speech language therapy' is a real, specific, nameable service commonly covered under home health care. The 'Page 121' appears to be an index/page reference artifact appended by extraction, but the underlying name refers to a genuine benefit.

## "Sperm washing" -> benefit (confidence=high)
- Sperm washing is a specific, nameable medical procedure used in infertility treatment, appearing in a bulleted list of distinct services alongside artificial insemination and post-coital test. A member could clearly ask whether it is covered.

## "Spring-powered lancet devices" -> benefit (confidence=high)
- 'Spring-powered lancet devices' names a specific, tangible medical item used in diabetes management. Under an Outpatient Diabetes Management Program header, this is a concrete covered supply a member could point to and ask about. It is a real, nameable item, not a generic category or fragment.

## "Standard (one pair annually)" -> benefit (confidence=medium)
- Under the 'Contact Lenses' header, 'Standard (one pair annually)' refers to standard contact lenses with a one-pair-per-year frequency limit. This names a specific, coverable item (standard contact lenses), so it qualifies as a benefit despite the parenthetical frequency qualifier.

## "State-controlled drugs" -> benefit (confidence=medium)
- 'State-controlled drugs' names a specific, identifiable category of medications (controlled substances regulated by state law) that a member could ask about being covered. It appears under Prescription Drugs and refers to a nameable class of items rather than a process word or a fragment/criterion. Confidence is medium due to lack of direct excerpts.

## "Stayplates to replace recently extracted permanent anterior (front) teeth" -> benefit (confidence=high)
- The name refers to a specific, nameable dental appliance/service (stayplates used to replace recently extracted permanent anterior teeth). It appears under Class III Major Services, a benefit category. A member could point to this and ask if it's covered, so it qualifies as a real benefit.

## "Substance Use Disorder Partial Hospitalization Program (PHP)" -> benefit (confidence=high)
- This names a specific, nameable service -- a Partial Hospitalization Program for substance use disorder treatment. A member could point to it and ask whether it's covered. It appears under Behavioral Health Services and is a well-defined level of care, not a generic category or fragment.

## "Summary of findings" -> fragment_or_criterion (confidence=medium)
- 'Summary of findings' appears as a sub-item within an eye exam component list, describing part of the exam process/documentation rather than naming a specific covered service. It is not a nameable service a member would ask about, nor a distinct benefit. It reads as a fragment describing what an eye exam includes, not a benefit itself.

## "Supplements" -> generic_administrative (confidence=medium)
- "Supplements" appears as part of a category heading "Preventive Drugs, Immunization Vaccines, Supplements and Vitamins". On its own it is a broad generic category noun rather than a specific nameable service or item. It functions as a class of items in the prescription drug section rather than a distinct benefit a member could point to and ask about specifically.

## "Supplies" -> generic_administrative (confidence=high)
- 'Supplies' is a generic category noun, not a specific nameable service. It appears as part of a phrase 'Dialysis services... supplies and equipment' where the specific benefit is dialysis; 'supplies' alone is just a category word like 'equipment' or 'drugs'.

## "Supplies and equipment used for subacute detoxification or rehabilitation" -> benefit (confidence=medium)
- While 'Supplies and equipment' alone would be generic, this name specifies a concrete, nameable item tied to a specific service context ('used for subacute detoxification or rehabilitation'). A member could point to it and ask whether it's covered. It's a specific covered item within behavioral health services rather than a mere category word or a fragment/criterion.

## "Support garments or other nonmedical items" -> fragment_or_criterion (confidence=medium)
- The name 'Support garments or other nonmedical items' is vague and open-ended. While 'support garments' alone might be a nameable item, the 'or other nonmedical items' qualifier makes this a broad catch-all category rather than a specific, pointable service. It reads more like an exclusion clause describing a class of non-covered items than a distinct benefit name. Leaning toward fragment/criterion given the non-specific catch-all phrasing, though there is some doubt since 'support garments' is a real item.

## "Surgical and impacted tooth extractions and root removal" -> benefit (confidence=high)
- This names specific, nameable dental services (surgical/impacted tooth extractions and root removal) that a member could ask about coverage for. It appears in a Class III Major Services list of covered procedures.

## "Surgical endodontic services" -> benefit (confidence=high)
- 'Surgical endodontic services' names a specific, nameable dental service (treating teeth with diseased or damaged nerves, including apicoectomy, etc.). A member could ask whether it's covered. It appears under Class III – Major Services and describes a concrete procedure category tied to specific treatments.

## "Surgical exposure and facilitation of eruption of unerupted teeth" -> benefit (confidence=high)
- This names a specific, nameable dental surgical procedure (surgically exposing and facilitating eruption of unerupted teeth). It appears in a bulleted list of covered surgical services under Class III/II. It is a concrete service a member could ask about, not a category word or fragment.

## "Surgical periodontic services" -> benefit (confidence=high)
- 'Surgical periodontic services' names a specific, nameable dental service that treats diseases of the gums and supporting structures. It appears under Class III Major Services as a distinct covered service category. A member could point to it and ask if it's covered.

## "Surgical treatment of male gynecomastia" -> benefit (confidence=high)
- This names a specific, nameable surgical procedure (surgical treatment of male gynecomastia) that a member could ask about coverage for. It appears alongside other specific procedures like blepharoplasty, breast reduction, and panniculectomy.

## "Survey, including history, physical exam, and diagnostic laboratory studies" -> fragment_or_criterion (confidence=low)
- The name reads as a compound description of a diagnostic process ('Survey, including history, physical exam, and diagnostic laboratory studies') rather than a single specific nameable service. It lists components of an evaluation. Under an 'Allergy Testing and Therapy' header this appears to describe what an allergy survey/evaluation entails. It leans toward a descriptive/process phrase rather than a discrete benefit, but there is ambiguity since 'diagnostic laboratory studies' and 'physical exam' are somewhat concrete. Low confidence given no excerpts.
- **Not auto-flagged**: below the high/medium-confidence precision gate.

## "Syringes" -> benefit (confidence=high)
- Syringes is a specific, nameable medical item covered under the diabetes management program. A member could point to it and ask if it's covered. It's not a generic category word or a fragment/criterion.

## "T-cell depleted infusion" -> benefit (confidence=high)
- T-cell depleted infusion is a specific, nameable medical procedure used in transplant services. It appears in bulleted benefit lists alongside other specific services like donor lymphocyte infusion. A member could point to it and ask if it's covered.

## "Tear test" -> benefit (confidence=high)
- 'Tear test' is a specific, nameable diagnostic procedure performed as part of a contact lens fitting exam. It refers to a concrete service a member could point to, not a category noun or a criterion/fragment.

## "Telephone or face-to-face contact and group interventions" -> fragment_or_criterion (confidence=low)
- The name describes modes/methods of contact (telephone, face-to-face, group interventions) rather than a specific nameable service. It reads as a descriptor of how a service is delivered under Collaborative Care Management, not a distinct benefit itself. However, without direct snippets and given it could arguably be a service component, confidence is low.
- **Not auto-flagged**: below the high/medium-confidence precision gate.

## "Telephone, individual face-to-face, and group interventions" -> benefit (confidence=medium)
- The name describes specific delivery modes of intervention services (telephone, face-to-face, group), which are nameable service formats a member could ask about, likely tobacco cessation or wellness counseling under Value Based Programs. It's more specific than a generic category word and doesn't read as a fragment or eligibility criterion, so I lean toward benefit with moderate confidence given lack of direct excerpts.

## "Temporary Benefits for Hospital Services:" -> fragment_or_criterion (confidence=medium)
- The name refers to a transitional/continuity-of-care provision describing a scenario (when a hospital ends its BCBS contract while you're receiving services) rather than naming a specific, distinct covered service. It's a process/administrative provision about temporary continuation of benefits, not a nameable medical service a member would point to and ask 'is this covered?' It leans toward administrative/criterion territory, but I keep confidence medium given ambiguity.

## "Temporomandibular surgery" -> benefit (confidence=high)
- Temporomandibular surgery is a specific, nameable surgical service (surgery of the temporomandibular joint) that a member could ask about coverage for. It appears alongside other specific benefits like bariatric surgery and infertility treatment.

## "Test strips and lancets" -> benefit (confidence=high)
- Test strips and lancets are specific, nameable diabetic supply items that a member could point to and ask if covered. Listed alongside other specific items like glucose monitors and insulin delivery reservoirs.

## "Test strips for glucometer" -> benefit (confidence=high)
- Test strips for glucometer names a specific, tangible diabetic supply item that a member could point to and ask if covered. It appears in a bulleted list alongside other concrete items like glucometers and lancets.

## "Test strips for glucose monitors" -> benefit (confidence=high)
- 'Test strips for glucose monitors' is a specific, nameable item that a member could ask about coverage for. It appears in a list of concrete diabetes supplies alongside insulin pumps, lancets, and monitors, all specific covered items.

## "Testing of visual acuity" -> benefit (confidence=high)
- Testing of visual acuity is a specific, nameable diagnostic service/procedure performed as part of an eye exam. It refers to a concrete service a member could point to, not a generic category word or a fragment/criterion.

## "The appropriateness of a drug for your condition" -> fragment_or_criterion (confidence=high)
- This is a sub-bullet describing something a medication assessment identifies, not a nameable covered service. It's a fragment/qualifier ('the appropriateness of a drug for your condition') rather than a specific service a member could point to and ask if it's covered.

## "The appropriateness of the drug for your condition" -> fragment_or_criterion (confidence=high)
- This is a sub-bullet describing something a medication assessment identifies, not a nameable service. It's a fragment describing an aspect/criterion evaluated within a service, alongside items like 'The correct dosage' and 'When to take the drug'. It does not name a specific service a member could point to.

## "The correct dosage" -> fragment_or_criterion (confidence=high)
- 'The correct dosage' is not a nameable service or item; it's a sub-bullet item in a list of assessment factors (appropriateness, dosage, timing, interactions). It describes a criterion/aspect being evaluated in a value-based program, not a specific covered benefit a member could ask about.

## "The correct drug dosage" -> fragment_or_criterion (confidence=high)
- This is an item in a list describing what assessments identify (appropriateness, correct dosage, timing, interactions), not a specific nameable service. It's a fragment describing a criterion/component of medication management, not a benefit itself.

## "The cost of developing and fitting the basic device" -> fragment_or_criterion (confidence=high)
- This is a cost/process description within a list of what is covered under prosthetic/orthotic devices, not a specific nameable service. 'The cost of developing and fitting the basic device' describes a cost component rather than a distinct benefit a member could point to and ask about.

## "The cost of purchasing or replacing the device" -> fragment_or_criterion (confidence=high)
- The name 'The cost of purchasing or replacing the device' describes a cost/scenario rather than naming a specific service or item. The actual benefit is the prosthetic/orthotic device itself; this phrase is a descriptive clause about paying for purchase/replacement, not a nameable service a member could point to.

## "The diagnosis of a condition" -> fragment_or_criterion (confidence=high)
- 'The diagnosis of a condition' describes an activity/scenario within an online visit context rather than naming a specific, coverable service or item. It's a fragment describing what the visit accomplishes, not a nameable benefit a member would point to and ask if covered.

## "The drug Interactions" -> fragment_or_criterion (confidence=high)
- This is one item in a list describing aspects of medication counseling/review ('The correct drug dosage', 'The right time to take the drug', 'The drug Interactions'). It is a fragment describing a topic covered during collaborative care management, not a specific nameable service a member could point to and ask if it's covered.

## "The experimental or investigational item, device or service" -> fragment_or_criterion (confidence=medium)
- The name is a descriptive phrase referencing 'the experimental or investigational item, device or service' rather than naming a specific covered service. Under a clinical trials routine patient costs section, this reads as a clause describing the scenario/exclusion (i.e., the experimental item itself isn't a routine patient cost), not a nameable benefit a member could point to. It functions as a qualifier/condition rather than a distinct service.

## "The provider is not a commercial airline" -> fragment_or_criterion (confidence=high)
- This is a condition/eligibility criterion for air ambulance coverage, not a nameable service. It appears in a bulleted list of requirements ('The provider is not a commercial airline', 'The member is taken to the nearest facility...'), describing qualifiers rather than naming a specific covered service.

## "The right time to take the drug" -> fragment_or_criterion (confidence=high)
- This is a sub-bullet describing an aspect of medication review/counseling within Collaborative Care Management, not a specific nameable service. It's a fragment describing what is evaluated, not a benefit a member could ask coverage for.

## "The subscriber directs BCBSM not to cover the newborn’s services" -> fragment_or_criterion (confidence=high)
- The name is a sentence describing a scenario/condition (the subscriber directing BCBSM not to cover services), not a specific nameable service or item. It clearly reads as an eligibility/coverage condition rather than a benefit.

## "Therapeutic boarding schools" -> benefit (confidence=high)
- 'Therapeutic boarding schools' is a specific, nameable type of facility/service that a member could point to and ask about coverage. Though it appears in exclusion lists, exclusion status must not drive classification. It names a concrete service, not a generic category or fragment.

## "Therapeutic care – Evidence-based services from licensed providers. It includes:" -> fragment_or_criterion (confidence=medium)
- The name ends with a colon and 'It includes:', indicating this was a header/lead-in phrase to a list of specific services rather than a nameable service itself. While 'Therapeutic care' relates to autism treatment, the trailing definitional phrasing 'Evidence-based services from licensed providers. It includes:' shows this is a description/category lead-in, not a specific pointable benefit.

## "Therapeutic injections" -> benefit (confidence=high)
- Therapeutic injections is a specific, nameable medical service that a member could ask about coverage for, appearing under Professional Services. It refers to a concrete clinical procedure, not a generic category or fragment.

## "Therapeutic pulpotomies or pulpal debridement" -> benefit (confidence=high)
- This names specific, nameable dental procedures (therapeutic pulpotomies and pulpal debridement) that a member could ask about being covered. It appears in a list of specific Class II basic services alongside other named procedures.

## "Therapy and counseling for family members" -> benefit (confidence=high)
- This names a specific, nameable service -- therapy and counseling provided to family members as part of behavioral health treatment. It appears alongside other specific services like individual/group therapy and psychological testing. A member could point to it and ask if it's covered.

## "Therapy that is performed without a physical therapy treatment" -> fragment_or_criterion (confidence=high)
- The name describes a scenario/condition (therapy performed without a physical therapy treatment) rather than naming a specific service. It appears in an exclusion list describing qualifiers, and does not point to a concrete, nameable service a member could ask about.

## "Therapy that is performed without a physical therapy treatment plan" -> fragment_or_criterion (confidence=high)
- The name describes a scenario/condition ('therapy performed without a treatment plan') rather than naming a specific, nameable service. It's a qualifier describing when therapy is excluded, not a service a member could point to and ask if covered.

## "Therapy that is performed without an occupational therapy treatment plan" -> fragment_or_criterion (confidence=high)
- The name describes a condition/scenario ('therapy performed without an occupational therapy treatment plan') rather than naming a specific service. It's an exclusion clause describing when therapy is not covered, not a nameable benefit.

## "Thyroid function" -> benefit (confidence=high)
- Thyroid function refers to a specific diagnostic test, listed alongside EKG, EEG, and pulmonary function studies under Diagnostic Services. It is a nameable, specific service a member could ask about.

## "Tobacco Cessation Programs" -> benefit (confidence=high)
- Tobacco Cessation Programs is a specific, nameable service (screening, counseling and prescription drugs to help stop smoking) under Preventive Care Services. A member could clearly ask whether this is covered.

## "Transcranial Magnetic Stimulation (TMS)" -> benefit (confidence=high)
- Transcranial Magnetic Stimulation (TMS) is a specific, nameable medical treatment/procedure used for behavioral health conditions. A member could clearly ask whether it is covered. The section header (Behavioral Health Services) is consistent with it being a real service.

## "Transitional living centers such as half-way and three-quarter way houses" -> benefit (confidence=medium)
- The name refers to a specific, nameable type of service/facility -- transitional living centers such as half-way and three-quarter way houses. Under a Behavioral Health Services header, this is a concrete facility/service a member could ask about, regardless of coverage status. It is not a generic category word nor a fragment/criterion.

## "Transplant surgery and related services performed in a non-designated facility" -> fragment_or_criterion (confidence=medium)
- The name describes transplant surgery performed under a specific scenario/condition ('in a non-designated facility'), which functions as a limitation/qualifier rather than naming a distinct covered service. The core service is 'transplant surgery,' and the added clause specifies where it is performed, making this a scenario/exclusion criterion rather than a specific nameable benefit.

## "Transplant surgery and related services performed in a nondesignated facility" -> fragment_or_criterion (confidence=medium)
- While 'Transplant surgery and related services' is a real benefit, this candidate name is qualified by 'performed in a nondesignated facility' — a scenario/condition describing where the service occurs rather than naming a distinct service. The excerpts confirm this is an exclusion scenario ('You have to pay for...if you receive...in a nondesignated facility'). The name describes a circumstance/qualifier rather than a specific nameable service, making it a fragment/criterion.

## "Transportation to and from a hospital or other facility" -> benefit (confidence=high)
- The name refers to a specific, nameable service (transportation to and from a hospital or other facility) that a member could point to and ask if it's covered. It appears in an exclusion list, but exclusion status must not affect classification. This is a concrete service, not a category word or a fragment/criterion.

## "Traumatic scars" -> benefit (confidence=high)
- "Traumatic scars" names a specific, nameable condition for which surgical treatment (e.g. reconstructive/scar revision) is provided. It appears in a Surgery section alongside other specific procedures/conditions like blepharoplasty and breast reduction. A member could point to it and ask whether treatment is covered. It is not a generic category word nor a fragment/criterion.

## "Travel and Lodging" -> benefit (confidence=medium)
- Travel and Lodging refers to a specific, reimbursable expense benefit (up to $5,000) associated with oncology clinical trials. A member could point to it and ask whether their travel/lodging is covered. While somewhat category-like, it names a concrete, reimbursable item with a defined limit, distinguishing it from purely generic administrative terms.

## "Treatment and consultation recommendations" -> fragment_or_criterion (confidence=medium)
- This phrase describes what an online visit consists of/produces rather than naming a specific covered service. It appears alongside 'The diagnosis of a condition' as components of a telehealth online visit. 'Treatment and consultation recommendations' is a descriptive fragment of what the provider delivers, not a distinct nameable benefit a member would point to and ask if it's covered.

## "Two single transplants" -> benefit (confidence=medium)
- 'Two single transplants' names a specific transplant service configuration for which covered services are provided when directly related to it. It appears in a list alongside 'Two tandem transplants', 'A single and a tandem transplant', and 'Allogeneic Transplants' -- all specific, nameable transplant scenarios/services a member could ask about. While it reads somewhat like a scenario, it refers to a concrete, identifiable transplant service arrangement rather than a generic category or an eligibility qualifier.

## "Two tandem transplants" -> benefit (confidence=medium)
- 'Two tandem transplants' refers to a specific, nameable transplant service configuration that a member could ask about coverage for. It appears alongside parallel specific items like 'Two single transplants' and 'A single and a tandem transplant', all naming concrete transplant scenarios rather than administrative categories or eligibility criteria. It names a real, specific procedure type.

## "Two visits for children 36 months through 47 months" -> fragment_or_criterion (confidence=high)
- This is a visit-frequency limitation for well-child visits (a quantity/age-range qualifier), not a nameable service. The underlying benefit is 'well-child visits'; this text merely specifies how many visits are allowed for a specific age range.

## "Two visits per member, per calendar year" -> fragment_or_criterion (confidence=high)
- This names a frequency/quantity limitation ('two visits per member, per calendar year'), not a specific nameable service. It describes a coverage limit rather than a benefit.

## "UV coating" -> benefit (confidence=high)
- UV coating is a specific, nameable lens option that a member could ask whether it's covered. It appears in a list of concrete lens options under the Lenses section, alongside other specific benefits like Progressive lenses and Anti-reflective lenses.

## "Ultrafiltration" -> benefit (confidence=high)
- Ultrafiltration is a specific, nameable medical procedure used in dialysis to remove fluid from the blood. It appears under Dialysis Services as a covered service. Unlike the generic entries alongside it (Equipment, Drugs, Supplies), it names a concrete procedure.

## "Ultrasound" -> benefit (confidence=high)
- Ultrasound is a specific, nameable diagnostic imaging service listed alongside other concrete radiology services like X-rays, CAT scans, and MRI. A member could clearly point to it and ask if it's covered.

## "Ultraviolet protective coating" -> benefit (confidence=high)
- Ultraviolet protective coating is a specific, nameable lens option/item that a member could ask about coverage for. It appears in a list of concrete lens options alongside polycarbonate lenses, anti-reflective coating, etc.

## "Umbilical cord blood" -> benefit (confidence=high)
- Umbilical cord blood is a specific, nameable item used in stem cell/transplant contexts. It appears alongside other harvested materials like peripheral blood stem cells as a concrete covered item a member could ask about.

## "Unstable angina" -> fragment_or_criterion (confidence=high)
- Unstable angina is a medical condition, not a covered service or item. It appears in a list of 'medical conditions' that serve as examples/criteria (likely for medically necessary hospital dental care). It does not name a specific service a member could ask to have covered; it describes a qualifying clinical scenario.

## "Up to eight hours of routine home care per day" -> benefit (confidence=medium)
- The name describes routine home care under hospice services, which is a specific, nameable service. The 'up to eight hours per day' is a quantity qualifier attached to a real service (routine home care). A member could ask 'is routine home care covered?' The service is identifiable, so it leans toward benefit despite the quantity framing.

## "Use of ambulatory surgery facility" -> benefit (confidence=medium)
- The name refers to use of an ambulatory surgery facility, which is a specific, nameable covered item/service that a member could ask about. It appears in a benefit list alongside other concrete services like anesthesia and recovery room. While phrased with 'Use of', it names a specific facility service rather than a generic category or a conditional fragment.

## "Visits through age 18 as follows:" -> fragment_or_criterion (confidence=high)
- The name 'Visits through age 18 as follows:' is a sentence fragment/lead-in introducing a list of visit allowances, not a specific nameable service. The actual benefit is 'Well-Baby and Well-Child Visits'; this candidate is just a qualifier describing the age scope and setting up a list.

## "Visual reading and urine test strips" -> benefit (confidence=high)
- This names a specific, tangible diabetic supply item (visual reading and urine test strips) listed alongside other concrete items like lancets, syringes, and insulin. A member could point to it and ask whether it is covered.

## "Vital pulpotomies on primary teeth" -> benefit (confidence=high)
- This names a specific, nameable dental procedure (vital pulpotomy performed on primary teeth), appearing under Class II Basic Services alongside other specific procedures. A member could clearly ask whether this procedure is covered.

## "Vitamins" -> benefit (confidence=medium)
- Vitamins is a specific, nameable item that a member could ask about coverage for (e.g., preventive vitamins covered under ACA). It refers to a concrete product category, not a process or cost-share term, and not a fragment or criterion. While somewhat broad, it names a specific item type rather than an administrative concept, so I lean toward benefit.

## "Well-Baby and Well-Child Visits" -> benefit (confidence=high)
- Well-Baby and Well-Child Visits are specific, nameable preventive care services that a member could ask about coverage for. This is a real benefit under Preventive Care Services, not a generic category or fragment.

## "X-rays" -> benefit (confidence=high)
- X-rays is a specific, nameable diagnostic imaging service that a member could point to and ask if it's covered. It appears under Radiology Services, consistent with a real benefit.

## "each visit, including:" -> fragment_or_criterion (confidence=high)
- The name 'each visit, including:' is a sentence fragment/lead-in phrase, not a specific nameable service. It describes a structure introducing a list rather than naming a covered service or item.

