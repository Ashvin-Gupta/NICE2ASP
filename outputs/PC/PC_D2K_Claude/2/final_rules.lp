

---------------Iteration 1----------------

I've reviewed the ASP rules and made some adjustments to ensure they accurately represent the guidelines. Here are the final rules:

[1.1.1]
offer("pancreatic_protocol_CT_scan") :- have("obstructive_jaundice"), suspected(cancer("pancreas")), not offered("draining_the_bile_duct").

[1.1.2]
1 {offer("FDG-PET/CT"); offer("EUS_with_EUS-guided_tissue_sampling")} 2 :- have("obstructive_jaundice"), suspected(cancer("pancreas")), offered("pancreatic_protocol_CT_scan"), findings_from_procedure("pancreatic_protocol_CT_scan", "unclear_diagnosis").

[1.1.3]
offer("biliary_brushing_for_cytology") :- have("obstructive_jaundice"), used_for("ERCP", "relieve_biliary_obstruction"), findings_from_procedure("ERCP", "no_tissue_diagnosis").

[1.1.4]
offer("pancreatic_protocol_CT_scan") :- have("pancreatic_abnormalities"), not have("jaundice").

[1.1.5]
1 {offer("FDG-PET/CT"); offer("EUS_with_EUS-guided_tissue_sampling")} 2 :- have("pancreatic_abnormalities"), not have("jaundice"), offered("pancreatic_protocol_CT_scan"), findings_from_procedure("pancreatic_protocol_CT_scan", "unclear_diagnosis").

[1.1.6]
offer("EUS_with_EUS-guided_tissue_sampling") :- have("pancreatic_abnormalities"), not have("jaundice"), need("cytological_or_histological_samples").

[1.1.7]
1 {offer("pancreatic_protocol_CT_scan"); offer("MRI/MRCP")} 1 :- have("pancreatic_cysts").
offer("MRI/MRCP") :- have("pancreatic_cysts"), offered("pancreatic_protocol_CT_scan"), need("more_information").
offer("pancreatic_protocol_CT_scan") :- have("pancreatic_cysts"), offered("MRI/MRCP"), need("more_information").

[1.1.8]
refer("resection") :- have("pancreatic_cysts"), have("obstructive_jaundice"), located_in("cystic_lesions", "head_of_the_pancreas").
refer("resection") :- have("pancreatic_cysts"), have("enhancing_solid_component_in_the_cyst").
refer("resection") :- have("pancreatic_cysts"), have("main_pancreatic_duct_that_is_10_mm_diameter_or_larger").

[1.1.9]
offer("EUS") :- have("pancreatic_cysts"), offered("CT"), offered("MRI/MRCP"), need("more_information_on_likelihood_of_malignancy").
offer("EUS") :- have("pancreatic_cysts"), offered("CT"), offered("MRI/MRCP"), not clear("whether_surgery_is_needed").

[1.1.10]
consider("fine-needle_aspiration") :- have("pancreatic_cysts"), offered("EUS"), need("more_information_on_likelihood_of_malignancy").

[1.1.11]
perform("CEA_assay") :- have("pancreatic_cysts"), performed("fine-needle_aspiration"), performed("cytology"), have("sufficient_sample").

[1.1.12]
follow("staging_recommendations") :- have("pancreatic_cysts"), thought_to_be("malignant").

[1.1.13]
ask("first-degree_relatives_with_pancreatic_cancer") :- diagnosed_with(cancer("pancreas")).

[1.1.14]
offer("surveillance", cancer("pancreas")) :- have("hereditary_pancreatitis"), have("PRSS1_mutation").
offer("surveillance", cancer("pancreas")) :- have("BRCA1_mutation"), first_degree_relative(cancer("pancreas"), N), N >= 1.
offer("surveillance", cancer("pancreas")) :- have("BRCA2_mutation"), first_degree_relative(cancer("pancreas"), N), N >= 1.
offer("surveillance", cancer("pancreas")) :- have("PALB2_mutation"), first_degree_relative(cancer("pancreas"), N), N >= 1.
offer("surveillance", cancer("pancreas")) :- have("CDKN2A_mutation"), first_degree_relative(cancer("pancreas"), N), N >= 1.
offer("surveillance", cancer("pancreas")) :- have("Peutz-Jeghers_syndrome").

[1.1.15]
consider("surveillance", cancer("pancreas")) :- first_degree_relative(cancer("pancreas"), N), N >= 2, across_generations(G), G >= 2.
consider("surveillance", cancer("pancreas")) :- have("Lynch_syndrome"), first_degree_relative(cancer("pancreas"), N), N >= 1.

[1.1.16]
1 {consider("MRI/MRCP"); consider("EUS")} 2 :- need("pancreatic_cancer_surveillance"), not have("hereditary_pancreatitis").

[1.1.17]
consider("pancreatic_protocol_CT_scan") :- need("pancreatic_cancer_surveillance"), have("hereditary_pancreatitis"), have("PRSS1_mutation").

[1.1.18]
:- have("hereditary_pancreatitis"), offer("EUS", "detect_pancreatic_cancer").

[1.3.1]
offer("pancreatic_protocol_CT_scan_including_chest_abdomen_pelvis") :- diagnosed_with(cancer("pancreas"), "newly"), not had("pancreatic_protocol_CT_scan").

[1.3.2]
offer("FDG-PET/CT") :- diagnosed_with(cancer("pancreas")), findings_from_procedure("CT", "localised_disease"), will_have("cancer_treatment").

[1.3.3]
consider("MRI") :- diagnosed_with(cancer("pancreas")), need("more_information_for_clinical_management"), have("suspected_liver_metastases").
consider("endoscopic_ultrasound") :- diagnosed_with(cancer("pancreas")), need("more_information_for_clinical_management"), need("tumour_and_node_staging").
consider("laparoscopy_with_laparoscopic_ultrasound") :- diagnosed_with(cancer("pancreas")), need("more_information_for_clinical_management"), have("suspected_small-volume_peritoneal_or_liver_metastases"), is_possibility("resectional_surgery").

[1.13.2]
carry_out("assessment_for_additional_symptoms") :- have("unexplained_weight_loss").
1 {offer("urgent_investigation"); offer("suspected_cancer_pathway_referral")} 1 :- have("unexplained_weight_loss").

[1.13.3]
carry_out("assessment_for_additional_symptoms") :- have("unexplained_appetite_loss").
1 {offer("urgent_investigation"); offer("suspected_cancer_pathway_referral")} 1 :- have("unexplained_appetite_loss").

[1.2.4]
refer("suspected_cancer_pathway_referral", cancer("pancreas")) :- age(X), X >= 40, have("jaundice").

[1.2.5]
consider("urgent_direct_access_CT_scan") :- age(X), X >= 60, have("weight_loss"), have(S), symptom(S), timeframe("within_2_weeks").
consider("urgent_ultrasound_scan") :- age(X), X >= 60, have("weight_loss"), have(S), symptom(S), not available("CT").

symptom("diarrhoea").
symptom("back_pain").
symptom("abdominal_pain").
symptom("nausea").
symptom("vomiting").
symptom("constipation").
symptom("new-onset_diabetes").

