import fs from 'node:fs'
import path from 'node:path'

const projectRoot = process.cwd()
const distRoot = path.join(projectRoot, 'dist')
const locales = ['en', 'fr']
const mainRoutePrefixes = new Set([
  '',
  'about',
  'book-a-call',
  'book-a-demo',
  'data-governance',
  'education',
  'ifitwala-ed',
  'implementation',
  'platform',
  'security',
  'services',
])

const replacements = [
  ['ERP Implementation for Schools and SMEs | Ifitwala', 'Implementation ERP pour ecoles et PME | Ifitwala'],
  ['Practical ERP implementation for SMEs and schools using Frappe, ERPNext, Odoo, workflow mapping, reporting, permissions, and data governance.', 'Implementation ERP concrete pour PME et ecoles utilisant Frappe, ERPNext, Odoo, cartographie des workflows, reporting, permissions et gouvernance des donnees.'],
  ['ERP Discovery and Implementation for SMEs | Ifitwala', 'Decouverte et implementation ERP pour PME | Ifitwala'],
  ['ERP discovery, Frappe, ERPNext and Odoo implementation, and data exposure audits for SMEs, schools, and teams handling sensitive operational data.', 'Decouverte ERP, implementation Frappe, ERPNext et Odoo, et audits d exposition des donnees pour PME, ecoles et equipes gerant des donnees operationnelles sensibles.'],
  ['Frappe, ERPNext and Odoo Implementation for SMEs | Ifitwala', 'Implementation Frappe, ERPNext et Odoo pour PME | Ifitwala'],
  ['Open-source ERP implementation for SMEs and schools using Frappe, ERPNext, Odoo, HRMS, CRM, LMS, and Moodle, from discovery to migration, UAT, training, and go-live.', 'Implementation ERP open source pour PME et ecoles utilisant Frappe, ERPNext, Odoo, HRMS, CRM, LMS et Moodle, de la decouverte a la migration, aux tests utilisateurs, a la formation et au go-live.'],
  ['School ERP and Data Governance | Ifitwala', 'ERP scolaire et gouvernance des donnees | Ifitwala'],
  ['ERP Discovery, Implementation, and Data Governance | Ifitwala', 'Decouverte ERP, implementation et gouvernance des donnees | Ifitwala'],
  ['ERPNext and Odoo Implementation for Schools and SMEs | Ifitwala', 'Implementation ERPNext et Odoo pour ecoles et PME | Ifitwala'],
  ['Data Exposure Audit for ERP and School Operations | Ifitwala', 'Audit d exposition des donnees pour ERP et operations scolaires | Ifitwala'],
  ['Practical ERP implementation for schools and organizations handling sensitive data, with ERPNext, Odoo, workflow mapping, reporting, permissions, and governance.', 'Implementation ERP concrete pour les ecoles et organisations qui gerent des donnees sensibles, avec ERPNext, Odoo, cartographie des workflows, reporting, permissions et gouvernance.'],
  ['Ifitwala helps schools and organizations handling sensitive operational data implement ERP systems, improve workflows, and govern reporting, permissions, and data access across Frappe, ERPNext, Odoo, and related platforms.', 'Ifitwala aide les ecoles et organisations qui gerent des donnees operationnelles sensibles a implementer des systemes ERP, ameliorer les workflows et gouverner le reporting, les permissions et l acces aux donnees autour de Frappe, ERPNext, Odoo et plateformes associees.'],
  ['ERP implementation and data governance for schools', 'Implementation ERP et gouvernance des donnees pour ecoles'],
  ['School ERP implementation, ERP discovery sprint, ERPNext consulting, Odoo implementation, data exposure audit', 'Implementation ERP scolaire, sprint de decouverte ERP, conseil ERPNext, implementation Odoo, audit d exposition des donnees'],
  ['Practical ERP implementation for schools and organizations handling sensitive data.', 'Implementation ERP concrete pour les ecoles et organisations qui gerent des donnees sensibles.'],
  ['We help teams replace spreadsheets and disconnected systems with ERPNext or Odoo, while improving reporting, permissions, and operational control.', 'Nous aidons les equipes a remplacer tableurs et systemes deconnectes par ERPNext ou Odoo, tout en ameliorant le reporting, les permissions et le controle operationnel.'],
  ['Book a 15-minute fit call', 'Reserver un appel de cadrage de 15 min'],
  ['Explore the discovery sprint', 'Explorer le sprint de decouverte'],
  ['School operations, admissions, and reporting', 'Operations scolaires, admissions et reporting'],
  ['ERPNext, Frappe, and practical Odoo support', 'ERPNext, Frappe et support Odoo pratique'],
  ['Role-based access and GDPR-aware controls', 'Acces par role et controles compatibles RGPD'],
  ['Start with the wedge', 'Commencer par le point d entree'],
  ['Clarity before implementation.', 'Clarifier avant d implementer.'],
  ['Buyers rarely start by asking for GDPR or a full ERP rollout. They start with admissions chaos, unreliable reports, duplicated data, unclear ownership, and too many spreadsheets. The first offer should make the problem legible.', 'Les acheteurs commencent rarement par demander le RGPD ou un deploiement ERP complet. Ils commencent par des admissions chaotiques, des rapports peu fiables, des donnees dupliquees, des responsabilites floues et trop de tableurs. La premiere offre doit rendre le probleme lisible.'],
  ['ERP Discovery Sprint', 'Sprint de decouverte ERP'],
  ['Map processes, identify risks, compare platform options, and leave with a realistic implementation roadmap before committing to a larger ERP project.', 'Cartographier les processus, identifier les risques, comparer les options de plateforme et repartir avec une feuille de route realiste avant de s engager dans un projet ERP plus large.'],
  ['Deploy ERPNext, Frappe, or Odoo around the workflows that matter first: admissions, finance, operations, reporting, roles, and adoption.', 'Deployer ERPNext, Frappe ou Odoo autour des workflows prioritaires : admissions, finance, operations, reporting, roles et adoption.'],
  ['Data Exposure Audit', 'Audit d exposition des donnees'],
  ['Review permissions, exports, reporting access, ownership, and data handling practices so sensitive operational data is easier to control.', 'Revoir les permissions, exports, acces aux rapports, responsabilites et pratiques de traitement afin de mieux controler les donnees operationnelles sensibles.'],
  ['Strongest unfair advantage', 'Avantage le plus difficile a copier'],
  ['Start with school operations, then expand where the fit is clear.', 'Commencer par les operations scolaires, puis elargir lorsque l adequation est claire.'],
  ['That environment demands more than software configuration. It requires clean workflows, reliable records, role-based access, reporting controls, and privacy-aware processes that staff can actually follow.', 'Cet environnement exige plus qu une configuration logicielle. Il demande des workflows clairs, des dossiers fiables, des acces par role, des controles de reporting et des processus respectueux de la confidentialite que les equipes peuvent vraiment suivre.'],
  ['That is the wedge: Ifitwala can speak the language of school leadership, admissions, operations, and data ownership in a way generic ERP implementers usually cannot.', 'C est le point d entree : Ifitwala peut parler le langage de la direction scolaire, des admissions, des operations et de la responsabilite des donnees d une maniere que les integrateurs ERP generalistes maitrisent rarement.'],
  ['Ifitwala Ed keeps the positioning grounded.', 'Ifitwala Ed garde le positionnement ancre dans le concret.'],
  ['Ifitwala Ed is our education ERP, built from direct international-school experience. It gives the service business practical credibility without forcing Ifitwala to compete as just another Odoo partner.', 'Ifitwala Ed est notre ERP education, construit a partir d une experience directe en ecole internationale. Il donne une credibilite concrete aux services sans obliger Ifitwala a se presenter comme un partenaire Odoo de plus.'],
  ['Not sure whether this is an ERP, data, or workflow problem?', 'Vous ne savez pas si c est un probleme ERP, donnees ou workflow ?'],
  ['Bring the messy workflow, scattered data, uncertain platform decision, or stalled implementation. The first call is about finding the smallest credible next step.', 'Apportez le workflow confus, les donnees dispersees, la decision de plateforme incertaine ou l implementation bloquee. Le premier appel sert a trouver la plus petite prochaine etape credible.'],
  ['ERP discovery, ERPNext and Odoo implementation, and data exposure audits for schools and organizations handling sensitive operational data.', 'Decouverte ERP, implementation ERPNext et Odoo, et audits d exposition des donnees pour les ecoles et organisations qui gerent des donnees operationnelles sensibles.'],
  ['Ifitwala helps schools and organizations handling sensitive data replace scattered workflows with clearer ERP, reporting, permissions, and operational control.', 'Ifitwala aide les ecoles et organisations qui gerent des donnees sensibles a remplacer des workflows disperses par un ERP, un reporting, des permissions et un controle operationnel plus clairs.'],
  ['From messy work to controlled systems', 'Du travail disperse aux systemes controles'],
  ['Core offers', 'Offres principales'],
  ['Start small enough to reduce risk, then implement what is proven.', 'Commencer assez petit pour reduire le risque, puis implementer ce qui est prouve.'],
  ['The discovery sprint is the first offer because it sells clarity, not a premature platform commitment. Full implementation follows when the workflow, data, and ownership questions are clear.', 'Le sprint de decouverte est la premiere offre parce qu il vend de la clarte, pas un engagement premature sur une plateforme. L implementation complete suit lorsque les questions de workflow, de donnees et de responsabilite sont claires.'],
  ['A focused first step: map the messy process, identify risk, compare ERPNext/Odoo/Frappe options, and leave with a realistic roadmap before committing to a bigger project.', 'Une premiere etape ciblee : cartographier le processus confus, identifier les risques, comparer les options ERPNext/Odoo/Frappe et repartir avec une feuille de route realiste avant de s engager dans un projet plus large.'],
  ['Best first wedge', 'Meilleur point d entree initial'],
  ['School ERP and admissions systems come first.', 'L ERP scolaire et les admissions passent en premier.'],
  ['Education is where the expertise is hardest to copy.', 'L education est le domaine ou l expertise est la plus difficile a copier.'],
  ['Admissions, student records, guardians, staff, safeguarding-adjacent data, reporting, finance, and access control create the kind of people-process-data complexity that Ifitwala is built to handle.', 'Admissions, dossiers eleves, responsables legaux, personnel, donnees proches du safeguarding, reporting, finance et controle d acces creent le type de complexite personnes-processus-donnees pour lequel Ifitwala est construit.'],
  ['Explore education systems', 'Explorer les systemes educatifs'],
  ['Start with a fit call. We can separate workflow problems, data problems, platform problems, and adoption problems before recommending a path.', 'Commencez par un appel de cadrage. Nous pouvons separer les problemes de workflow, de donnees, de plateforme et d adoption avant de recommander un chemin.'],
  ['ERP implementation after the workflow is clear.', 'Implementation ERP une fois le workflow clarifie.'],
  ['We help schools and SMEs implement Frappe, ERPNext, Odoo, LMS platforms, and education operations systems with a practical focus on workflows, data quality, permissions, reporting, and adoption.', 'Nous aidons les ecoles et PME a implementer Frappe, ERPNext, Odoo, des plateformes LMS et des systemes d operations educatives avec une attention concrete aux workflows, a la qualite des donnees, aux permissions, au reporting et a l adoption.'],
  ['Start with discovery', 'Commencer par la decouverte'],
  ['Know who can see, export, change, and report on sensitive data.', 'Savoir qui peut voir, exporter, modifier et reporter sur les donnees sensibles.'],
  ['We help schools and organizations understand where operational and people data lives, who can access it, how it moves, and where exposure risks need attention.', 'Nous aidons les ecoles et organisations a comprendre ou vivent les donnees operationnelles et personnelles, qui peut y acceder, comment elles circulent et ou les risques d exposition demandent de l attention.'],
  ['Request an exposure review', 'Demander une revue d exposition'],
  ['Governance as practical system behavior.', 'La gouvernance comme comportement systeme concret.'],
  ['GDPR readiness becomes useful when it is translated into concrete behavior: access, retention, exports, ownership, reporting, and data movement.', 'La preparation RGPD devient utile lorsqu elle se traduit en comportements concrets : acces, conservation, exports, responsabilite, reporting et circulation des donnees.'],
  ['Book a fit call', 'Reserver un appel de cadrage'],
  ['Bring the messy systems question. Leave with a clearer next step.', 'Apportez la question systeme confuse. Repartez avec une prochaine etape plus claire.'],
  ['Use this 15-minute call to decide whether the next move is discovery, ERP implementation, a data exposure audit, or simply a better way to frame the problem.', 'Utilisez cet appel de 15 minutes pour decider si la prochaine etape est une decouverte, une implementation ERP, un audit d exposition des donnees ou simplement une meilleure maniere de formuler le probleme.'],
  ['Book a 15-minute fit call with Ifitwala to discuss school ERP, ERP discovery, ERPNext, Odoo, workflow improvement, or data exposure risks.', 'Reservez un appel de cadrage de 15 minutes avec Ifitwala pour discuter ERP scolaire, decouverte ERP, ERPNext, Odoo, amelioration des workflows ou risques d exposition des donnees.'],
  ['Three fields, two selectors, then we can decide whether there is a fit.', 'Trois champs, deux selecteurs, puis nous pouvons voir s il y a une bonne adequation.'],
  ['Request fit call', 'Demander un appel de cadrage'],
  ['ERP Implementation Services for SMEs | Ifitwala', 'Services d implementation ERP pour PME | Ifitwala'],
  ['Frappe, ERPNext and Odoo Implementation for SMEs | Ifitwala', 'Implementation Frappe, ERPNext et Odoo pour PME | Ifitwala'],
  ['About Ifitwala | ERP Implementation for SMEs', 'A propos d Ifitwala | Implementation ERP pour PME'],
  ['ERP Data Governance and Privacy Readiness | Ifitwala', 'Gouvernance des donnees ERP et preparation confidentialite | Ifitwala'],
  ['Education ERP, SIS and LMS Implementation | Ifitwala', 'Implementation ERP education, SIS et LMS | Ifitwala'],
  ['Ifitwala Ed | Education ERP for School Operations', 'Ifitwala Ed | ERP education pour les operations scolaires'],
  ['ERP Implementation Approach for Schools | Ifitwala Ed', 'Approche d implementation ERP pour ecoles | Ifitwala Ed'],
  ['Education ERP Security and Trust | Ifitwala Ed', 'Securite et confiance ERP education | Ifitwala Ed'],
  ['Book an ERP Implementation Call | Ifitwala', 'Reserver un appel implementation ERP | Ifitwala'],
  ['Book an Ifitwala Ed Education ERP Demo', 'Reserver une demo ERP education Ifitwala Ed'],
  ['ERP consulting for SMEs across Frappe, ERPNext, Odoo, workflow improvement, data governance, migration planning, UAT, training, and go-live.', 'Conseil ERP pour PME autour de Frappe, ERPNext, Odoo, amelioration des workflows, gouvernance des donnees, planification de migration, tests utilisateurs, formation et go-live.'],
  ['Open-source ERP implementation for SMEs using Frappe, ERPNext, Odoo, HRMS, CRM, LMS, and Moodle, from discovery to migration, UAT, training, and go-live.', 'Implementation ERP open source pour PME utilisant Frappe, ERPNext, Odoo, HRMS, CRM, LMS et Moodle, de la decouverte a la migration, aux tests utilisateurs, a la formation et au go-live.'],
  ['Ifitwala helps SMEs and schools implement Frappe, ERPNext, Odoo, and education ERP systems with workflow mapping, data governance, and adoption support.', 'Ifitwala aide les PME et les ecoles a implementer Frappe, ERPNext, Odoo et des systemes ERP education avec cartographie des workflows, gouvernance des donnees et soutien a l adoption.'],
  ['ERP data governance and privacy-readiness support for SMEs and schools handling sensitive people, finance, customer, and operational data.', 'Accompagnement en gouvernance des donnees ERP et preparation confidentialite pour PME et ecoles gerant des donnees personnelles, financieres, clients et operationnelles sensibles.'],
  ['ERP, SIS, LMS, admissions, reporting, safeguarding workflows, and privacy-aware data operations for schools and education organizations.', 'ERP, SIS, LMS, admissions, reporting, workflows de safeguarding et operations de donnees respectueuses de la confidentialite pour les ecoles et organisations educatives.'],
  ['Ifitwala Ed is an education ERP for school operations, admissions, student records, portals, workflows, reporting, and governed school data.', 'Ifitwala Ed est un ERP education pour les operations scolaires, les admissions, dossiers eleves, portails, workflows, reporting et donnees scolaires gouvernees.'],
  ['Understand the Ifitwala Ed rollout approach for schools, from discovery, workflow mapping, configuration, migration, and UAT to adoption.', 'Comprendre l approche de deploiement d Ifitwala Ed pour les ecoles, de la decouverte, cartographie des workflows, configuration, migration et tests utilisateurs jusqu a l adoption.'],
  ['Review education ERP security and trust topics for Ifitwala Ed: permissions, operational continuity, ownership, accountability, and support.', 'Revoir les sujets de securite et confiance ERP education pour Ifitwala Ed : permissions, continuite operationnelle, responsabilite, redevabilite et support.'],
  ['Book a call with Ifitwala to discuss SME ERP implementation, Frappe, ERPNext, Odoo, workflow improvement, data governance, or education systems.', 'Reservez un appel avec Ifitwala pour discuter implementation ERP PME, Frappe, ERPNext, Odoo, amelioration des workflows, gouvernance des donnees ou systemes educatifs.'],
  ['Schedule a product demo of Ifitwala Ed, the education ERP for admissions, student records, portals, workflows, reporting, and school data governance.', 'Planifiez une demo produit d Ifitwala Ed, l ERP education pour admissions, dossiers eleves, portails, workflows, reporting et gouvernance des donnees scolaires.'],
  ['ERP implementation FAQ', 'FAQ implementation ERP'],
  ['Common questions from SME ERP research.', 'Questions frequentes issues de la recherche ERP pour PME.'],
  ['Does Ifitwala implement Frappe and ERPNext?', 'Ifitwala implemente-t-il Frappe et ERPNext ?'],
  ['Yes. Ifitwala implements Frappe Framework applications, ERPNext, and related Frappe tools including HRMS, CRM, LMS, and Helpdesk.', 'Oui. Ifitwala implemente des applications Frappe Framework, ERPNext et les outils Frappe associes, dont HRMS, CRM, LMS et Helpdesk.'],
  ['Does Ifitwala support Odoo implementation?', 'Ifitwala accompagne-t-il l implementation Odoo ?'],
  ['Yes. Ifitwala supports Odoo implementation projects where organizations need strong workflow mapping, migration planning, permissions design, testing, training, and go-live coordination.', 'Oui. Ifitwala accompagne les projets d implementation Odoo lorsque les organisations ont besoin d une cartographie solide des workflows, d une planification de migration, d un design des permissions, de tests, de formation et de coordination go-live.'],
  ['Who is this ERP implementation service for?', 'A qui s adresse ce service d implementation ERP ?'],
  ['The service is for SMEs, schools, and operational teams that need clearer workflows, cleaner data, better access control, reporting, and adoption support during ERP implementation.', 'Ce service s adresse aux PME, ecoles et equipes operationnelles qui ont besoin de workflows plus clairs, de donnees plus propres, d un meilleur controle d acces, de reporting et de soutien a l adoption pendant l implementation ERP.'],
  ['Ifitwala | ERP, data governance, and operational systems', 'Ifitwala | ERP, gouvernance des donnees et systemes operationnels'],
  ['Education ERP Platform for School Operations | Ifitwala Ed', 'Plateforme ERP education pour les operations scolaires | Ifitwala Ed'],
  ['ERP Implementation for SMEs | Frappe, Odoo | Ifitwala', 'Implementation ERP pour PME | Frappe, Odoo | Ifitwala'],
  ['Open-source ERP Implementation | Ifitwala', 'Implementation ERP open source | Ifitwala'],
  ['Explore how Ifitwala Ed connects academics, operations, finance, communication, admissions, student records, and institutional reporting in one platform.', 'Decouvrez comment Ifitwala Ed connecte pedagogie, operations, finance, communication, admissions, dossiers eleves et reporting institutionnel dans une seule plateforme.'],
  ['Explore how Ifitwala Ed connects academics, operations, finance, communication, and institutional reporting in one platform.', 'Decouvrez comment Ifitwala Ed connecte pedagogie, operations, finance, communication et reporting institutionnel dans une seule plateforme.'],
  ['Understand the rollout approach behind Ifitwala Ed, from discovery and configuration to adoption and institutional ownership.', 'Comprendre l approche de deploiement d Ifitwala Ed, de la decouverte et de la configuration jusqu a l adoption et a l appropriation institutionnelle.'],
  ['Review the trust conversation institutions should have when evaluating Ifitwala Ed: permissions, operational continuity, ownership, and support.', 'Revoir la discussion de confiance que les institutions devraient mener lorsqu elles evaluent Ifitwala Ed : permissions, continuite operationnelle, responsabilite et support.'],
  ['ERP, data governance, and operations delivery', 'ERP, gouvernance des donnees et execution operationnelle'],
  ['Operational systems for organizations that have outgrown scattered work.', 'Des systemes operationnels pour les organisations qui depassent le travail disperse.'],
  ['Ifitwala designs and delivers ERP-driven operational systems across Frappe Apps (ERPNext, HRMS, CRM), Odoo with a particular focus on education platforms, data governance, business analysis, and project delivery.', 'Ifitwala concoit et livre des systemes operationnels pilotes par l ERP autour de Frappe Apps (ERPNext, HRMS, CRM), Odoo, avec une attention particuliere aux plateformes educatives, a la gouvernance des donnees, a l analyse metier et a la conduite de projet.'],
  ['Explore our services', 'Explorer nos services'],
  ['See Ifitwala Ed', 'Voir Ifitwala Ed'],
  ['What we do', 'Ce que nous faisons'],
  ['From process reality to governed ERP delivery.', 'De la realite des processus a une livraison ERP gouvernee.'],
  ['Software implementation fails when the operational reality is unclear. We help organizations define the work, implement the system, manage delivery, and govern the data that runs through it.', 'Une implementation logicielle echoue lorsque la realite operationnelle est floue. Nous aidons les organisations a definir le travail, implementer le systeme, piloter la livraison et gouverner les donnees qui le traversent.'],
  ['Business Analysis', 'Analyse metier'],
  ['ERP Implementation', 'Implementation ERP'],
  ['Project Management', 'Gestion de projet'],
  ['Data Governance', 'Gouvernance des donnees'],
  ['Learn more', 'En savoir plus'],
  ['Deepest domain', 'Domaine de predilection'],
  ['Education is where our systems thinking was tested hardest.', 'L education est le domaine ou notre pensee systeme a ete le plus fortement mise a l epreuve.'],
  ['Schools and education groups carry dense operational data: applicants, students, guardians, staff, attendance, assessment, finance, learning platforms, wellbeing records, and leadership reporting.', 'Les ecoles et groupes educatifs portent des donnees operationnelles denses : candidats, eleves, responsables legaux, personnel, presence, evaluation, finance, plateformes d apprentissage, dossiers de bien-etre et reporting de direction.'],
  ['That environment demands more than configuration. It requires strong permissions, clean workflows, reliable records, privacy-aware access, and reporting that leaders can trust.', 'Cet environnement exige plus qu une configuration. Il demande des permissions solides, des workflows clairs, des dossiers fiables, des acces respectueux de la confidentialite et un reporting fiable pour la direction.'],
  ['This gives Ifitwala a practical base for organizations outside education that face similar people-process-data complexity.', 'Cela donne a Ifitwala une base pratique pour accompagner des organisations hors education confrontees a une complexite similaire entre personnes, processus et donnees.'],
  ['Flagship product', 'Produit phare'],
  ['Ifitwala Ed proves the work.', 'Ifitwala Ed prouve le travail.'],
  ['Ifitwala Ed is our full education ERP, built from direct international-school experience. It is proof that we do not only advise on systems, workflows, and data governance', 'Ifitwala Ed est notre ERP complet pour l education, construit a partir d une experience directe en ecole internationale. Il montre que nous ne faisons pas seulement du conseil sur les systemes, les workflows et la gouvernance des donnees'],
  ['Explore Ifitwala Ed', 'Explorer Ifitwala Ed'],
  ['Book a demo', 'Reserver une demo'],
  ['Book a Demo', 'Reserver une demo'],
  ['Book a Call', 'Reserver un appel'],
  ['Book a call', 'Reserver un appel'],
  ['Need a clearer path from operations to implementation?', 'Besoin d un chemin plus clair entre operations et implementation ?'],
  ['Bring the messy workflow, scattered data, uncertain ERP decision, or stalled implementation. We will help you identify the next practical step.', 'Apportez un workflow confus, des donnees dispersees, une decision ERP incertaine ou une implementation bloquee. Nous vous aidons a identifier la prochaine etape concrete.'],
  ['From school reality to ERP design', 'De la realite scolaire au design ERP'],
  ['Admissions and enrolment workflows', 'Workflows d admissions et d inscription'],
  ['Student, guardian, and staff records', 'Dossiers eleves, responsables et personnel'],
  ['Role-based access and permissions', 'Acces et permissions par role'],
  ['Reporting, data quality, and governance', 'Reporting, qualite des donnees et gouvernance'],

  ['Services | Ifitwala', 'Services | Ifitwala'],
  ['Services', 'Services'],
  ['Practical help with ERP, workflows, and governed data.', 'Une aide concrete pour l ERP, les workflows et les donnees gouvernees.'],
  ['Ifitwala supports organizations that need practical help with ERP implementation, workflow clarity, and governance for sensitive operational data.', 'Ifitwala accompagne les organisations qui ont besoin d une aide concrete pour l implementation ERP, la clarte des workflows et la gouvernance des donnees operationnelles sensibles.'],
  ['Service work, from process to reporting', 'Du processus au reporting'],
  ['Talk to us', 'Parlez-nous'],
  ['Open-source ERP Implementation', 'Implementation ERP open source'],
  ['ERP implementation for organizations that need systems people actually use.', 'Implementation ERP pour les organisations qui ont besoin de systemes reellement utilises.'],
  ['Discuss your implementation', 'Discuter de votre implementation'],
  ['See all services', 'Voir tous les services'],
  ['We do not only implement Frappe. We build on it.', 'Nous ne faisons pas qu implementer Frappe. Nous construisons avec Frappe.'],
  ['Frappe-first expertise, with practical Odoo and LMS implementation support.', 'Une expertise prioritaire sur Frappe, avec un support pratique pour Odoo et les LMS.'],
  ['Implementation work', 'Travail d implementation'],
  ['The platform matters, but the implementation discipline matters more.', 'La plateforme compte, mais la discipline d implementation compte davantage.'],

  ['Platform | Ifitwala Ed', 'Plateforme | Ifitwala Ed'],
  ['Platform overview', 'Vue d ensemble de la plateforme'],
  ['Platform', 'Plateforme'],
  ['A connected platform for running modern institutions.', 'Une plateforme connectee pour piloter des institutions modernes.'],
  ['Ifitwala Ed is designed to bring the workflows that usually live in disconnected systems into one calmer, more structured operating surface.', 'Ifitwala Ed est concu pour reunir les workflows souvent disperses dans des systemes separes au sein d une surface operationnelle plus calme et plus structuree.'],
  ['See Implementation', 'Voir l implementation'],
  ['Why this matters', 'Pourquoi c est important'],
  ['Leadership Visibility', 'Visibilite pour la direction'],
  ['Operational Consistency', 'Coherence operationnelle'],
  ['Cleaner Coordination', 'Coordination plus claire'],
  ['Confident Growth', 'Croissance plus sure'],
  ['Core platform pillars', 'Piliers de la plateforme'],
  ['Everything your institution needs to run in sync.', 'Tout ce dont votre institution a besoin pour fonctionner en coherence.'],
  ['Student Records', 'Dossiers eleves'],
  ['Academics and Assessment', 'Academique et evaluation'],
  ['Admissions and Enrollment', 'Admissions et inscriptions'],
  ['Finance and Billing', 'Finance et facturation'],
  ['Operations and Administration', 'Operations et administration'],
  ['Communication and Reporting', 'Communication et reporting'],
  ['How teams use it', 'Comment les equipes l utilisent'],
  ['Built for every team that keeps an institution moving.', 'Construit pour chaque equipe qui fait avancer une institution.'],
  ['Workflow coverage', 'Couverture des workflows'],
  ['The operating areas institutions need to evaluate clearly.', 'Les domaines operationnels que les institutions doivent evaluer clairement.'],
  ['Next step', 'Prochaine etape'],
  ['See the platform in the context of your institution.', 'Voir la plateforme dans le contexte de votre institution.'],

  ['Implementation | Ifitwala Ed', 'Implementation | Ifitwala Ed'],
  ['Implementation', 'Implementation'],
  ['Roll out with structure, not improvisation.', 'Deployer avec structure, pas avec improvisation.'],
  ['Institutional software only creates confidence when the rollout model is credible. The implementation conversation should cover structure, ownership, adoption, and the workflows that matter first.', 'Un logiciel institutionnel ne cree de la confiance que lorsque le modele de deploiement est credible. La discussion d implementation doit couvrir la structure, les responsabilites, l adoption et les workflows prioritaires.'],
  ['Phased rollout', 'Deploiement par phases'],
  ['Discovery', 'Decouverte'],
  ['Configuration', 'Configuration'],
  ['Adoption', 'Adoption'],
  ['Implementation principles', 'Principes d implementation'],
  ['A better rollout starts with the institution, not the software demo.', 'Un meilleur deploiement commence par l institution, pas par la demo logicielle.'],
  ['Who should be involved', 'Qui doit etre implique'],
  ['The right rollout is cross-functional.', 'Un bon deploiement est transversal.'],
  ['What strong rollout produces', 'Ce qu un bon deploiement produit'],
  ['Outcomes leadership can trust.', 'Des resultats fiables pour la direction.'],
  ['Review the rollout approach for your institution directly.', 'Revoir directement l approche de deploiement pour votre institution.'],
  ['Review trust and security', 'Revoir confiance et securite'],

  ['Security and Trust | Ifitwala Ed', 'Securite et confiance | Ifitwala Ed'],
  ['Security', 'Securite'],
  ['Security and trust', 'Securite et confiance'],
  ['Trust is part of the product decision.', 'La confiance fait partie de la decision produit.'],
  ['Institutions evaluating a platform should review more than features. The trust conversation should cover permissions, continuity, ownership, accountability, and operational support.', 'Les institutions qui evaluent une plateforme doivent aller au-dela des fonctionnalites. La discussion de confiance doit couvrir les permissions, la continuite, la responsabilite, la redevabilite et le support operationnel.'],
  ['What this page covers', 'Ce que couvre cette page'],
  ['Trust conversation', 'Discussion de confiance'],
  ['The institutional review should cover these areas clearly.', 'L evaluation institutionnelle doit couvrir clairement ces domaines.'],
  ['Evaluation checklist', 'Liste de controle d evaluation'],
  ['Questions every institution should ask during review.', 'Questions que chaque institution devrait poser pendant l evaluation.'],
  ['How to use this in the sales process', 'Comment l utiliser dans le processus commercial'],
  ['Use the evaluation to test operational seriousness.', 'Utiliser l evaluation pour tester le serieux operationnel.'],
  ['Review trust, permissions, and rollout expectations in a live walkthrough.', 'Examiner la confiance, les permissions et les attentes de deploiement lors d une demonstration en direct.'],

  ['Education Systems | Ifitwala', 'Systemes educatifs | Ifitwala'],
  ['Education systems', 'Systemes educatifs'],
  ['Education operations are where our systems work is deepest.', 'Les operations educatives sont le domaine ou notre travail systeme est le plus profond.'],
  ['Data Governance | Ifitwala', 'Gouvernance des donnees | Ifitwala'],
  ['Govern sensitive operational data with more confidence.', 'Gouverner les donnees operationnelles sensibles avec plus de confiance.'],
  ['About | Ifitwala', 'A propos | Ifitwala'],
  ['About Ifitwala', 'A propos d Ifitwala'],
  ['Book a Call | Ifitwala', 'Reserver un appel | Ifitwala'],
  ['Book a Demo | Ifitwala Ed', 'Reserver une demo | Ifitwala Ed'],
  ['Documentation', 'Documentation'],
  ['Home', 'Accueil'],
  ['Contact', 'Contact'],
  ['Github', 'Github'],
  ['All rights reserved.', 'Tous droits reserves.'],
  ['Features', 'Fonctionnalites'],
  ['Explore for more', 'En savoir plus'],
  ['> About <', '> A propos <'],

  ['From scattered work to trustworthy systems', 'Du travail disperse aux systemes fiables'],
  ['Map real operations, gaps, owners, and end-to-end processes.', 'Cartographier les operations reelles, les ecarts, les responsables et les processus de bout en bout.'],
  ['Implement Frappe, ERPNext, Odoo, roles, workflows, approvals, and reporting.', 'Implementer Frappe, ERPNext, Odoo, les roles, les workflows, les validations et le reporting.'],
  ['Control scope, milestones, risks, UAT, governance, and go-live.', 'Maitriser le perimetre, les jalons, les risques, les tests utilisateurs, la gouvernance et le go-live.'],
  ['Protect sensitive operational data through access control and GDPR/PDPA-aware workflows.', 'Proteger les donnees operationnelles sensibles grace au controle d acces et a des workflows compatibles RGPD/PDPA.'],

  ['Better systems start with clearer work.', 'De meilleurs systemes commencent par un travail plus clair.'],
  ['ERP implementation, workflow improvement, data governance, and education systems support from Ifitwala.', 'Implementation ERP, amelioration des workflows, gouvernance des donnees et accompagnement des systemes educatifs par Ifitwala.'],
  ['We help organizations map current workflows, define better processes, configure ERP systems, manage data migration, design roles and permissions, support testing, and prepare teams for go-live.', 'Nous aidons les organisations a cartographier les workflows actuels, definir de meilleurs processus, configurer les systemes ERP, gerer la migration des donnees, concevoir les roles et permissions, soutenir les tests et preparer les equipes au go-live.'],
  ['We help organizations understand where data lives, who can access it, how it moves, where exposure risks exist, and what practical controls should be put in place.', 'Nous aidons les organisations a comprendre ou vivent les donnees, qui peut y acceder, comment elles circulent, ou se trouvent les risques d exposition et quels controles pratiques mettre en place.'],
  ['Education Systems', 'Systemes educatifs'],
  ['We support schools and education organizations with ERP, SIS, LMS, admissions, reporting, data privacy, and workflow design.', 'Nous accompagnons les ecoles et organisations educatives sur l ERP, le SIS, les LMS, les admissions, le reporting, la confidentialite des donnees et le design des workflows.'],
  ['Not sure where your systems problem begins?', 'Vous ne savez pas ou commence votre probleme systeme ?'],
  ['Start with a call. We can help separate workflow problems, data problems, platform problems, and adoption problems.', 'Commencez par un appel. Nous pouvons distinguer les problemes de workflow, de donnees, de plateforme et d adoption.'],

  ['Sensitive data needs practical controls.', 'Les donnees sensibles ont besoin de controles pratiques.'],
  ['Data governance and privacy-readiness support for organizations handling sensitive operational and people data.', 'Accompagnement en gouvernance des donnees et preparation a la confidentialite pour les organisations qui gerent des donnees operationnelles et personnelles sensibles.'],
  ['We help organizations understand where operational and people data lives, who can access it, how it moves, and where privacy or exposure risks need attention.', 'Nous aidons les organisations a comprendre ou vivent les donnees operationnelles et personnelles, qui peut y acceder, comment elles circulent et ou les risques de confidentialite ou d exposition demandent de l attention.'],
  ['Request a governance review', 'Demander une revue de gouvernance'],
  ['Privacy-readiness, not empty compliance claims.', 'Preparation concrete a la confidentialite, pas de promesses de conformite vides.'],
  ['We support GDPR and PDPA readiness by focusing on concrete system behaviors: access, retention, exports, ownership, reporting, and data movement.', 'Nous soutenons la preparation RGPD et PDPA en nous concentrant sur des comportements systeme concrets : acces, conservation, exports, responsabilite, reporting et mouvement des donnees.'],
  ['Concrete offer', 'Offre concrete'],
  ['Data Exposure Audit', 'Audit d exposition des donnees'],
  ['A focused review for organizations that need to understand sensitive data risk before, during, or after ERP and workflow changes.', 'Une revue ciblee pour les organisations qui doivent comprendre les risques lies aux donnees sensibles avant, pendant ou apres des changements ERP et workflow.'],
  ['Map data locations', 'Cartographier les emplacements de donnees'],
  ['Identify where applicant, student, staff, guardian, customer, finance, and operational data lives.', 'Identifier ou vivent les donnees candidats, eleves, personnel, responsables, clients, finance et operations.'],
  ['Review access', 'Revoir les acces'],
  ['Check roles, permissions, exports, shared drives, reports, portals, and third-party tools.', 'Verifier les roles, permissions, exports, espaces partages, rapports, portails et outils tiers.'],
  ['Flag exposure risks', 'Signaler les risques d exposition'],
  ['Find excessive access, weak retention practices, unclear ownership, and risky data movement.', 'Identifier les acces excessifs, les pratiques de conservation faibles, les responsabilites floues et les mouvements de donnees risques.'],
  ['Plan remediation', 'Planifier la remediation'],
  ['Create a practical roadmap for controls, cleanup, reporting changes, and team habits.', 'Creer une feuille de route concrete pour les controles, le nettoyage, les changements de reporting et les habitudes d equipe.'],

  ['Education expertise', 'Expertise education'],
  ['Education is our deepest systems domain.', 'L education est notre domaine systeme le plus profond.'],
  ['ERP, SIS, LMS, admissions, reporting, safeguarding workflows, and privacy-aware data operations for education organizations.', 'ERP, SIS, LMS, admissions, reporting, workflows de safeguarding et operations de donnees respectueuses de la confidentialite pour les organisations educatives.'],
  ['We understand schools and education organizations because we have worked inside the overlap of admissions, student records, reporting, safeguarding workflows, staff operations, LMS ecosystems, and privacy-aware data management.', 'Nous comprenons les ecoles et organisations educatives parce que nous avons travaille au croisement des admissions, dossiers eleves, reporting, workflows de safeguarding, operations du personnel, ecosystemes LMS et gestion des donnees respectueuse de la confidentialite.'],
  ['School operations', 'Operations scolaires'],
  ['Admissions, student records, attendance, finance, staff workflows, parent communication, and leadership reporting.', 'Admissions, dossiers eleves, presence, finance, workflows du personnel, communication parents et reporting de direction.'],
  ['LMS and learning ecosystems', 'LMS et ecosystemes d apprentissage'],
  ['Moodle and LMS-adjacent workflows, data movement, reporting needs, and integration planning.', 'Moodle et workflows proches des LMS, circulation des donnees, besoins de reporting et planification des integrations.'],
  ['Sensitive people data', 'Donnees personnelles sensibles'],
  ['Student, staff, guardian, health, wellbeing, safeguarding, admissions, and assessment data all need careful governance.', 'Les donnees eleves, personnel, responsables, sante, bien-etre, safeguarding, admissions et evaluation demandent toutes une gouvernance attentive.'],
  ['Education ERP', 'ERP education'],
  ['Ifitwala Ed is our flagship product for schools that need one source of truth across daily operations.', 'Ifitwala Ed est notre produit phare pour les ecoles qui ont besoin d une source de verite unique dans les operations quotidiennes.'],
  ['Schools reveal the hardest parts of systems work.', 'Les ecoles revelent les parties les plus difficiles du travail systeme.'],
  ['Education data is personal, operational, time-sensitive, and distributed across many roles. A weak workflow can become a reporting issue, a privacy issue, or a student support issue.', 'Les donnees educatives sont personnelles, operationnelles, sensibles au temps et reparties entre de nombreux roles. Un workflow faible peut devenir un probleme de reporting, de confidentialite ou de soutien a l eleve.'],
  ['That makes education a strong base for broader ERP and governance work: it forces attention to permissions, adoption, data quality, reporting, and practical controls.', 'Cela fait de l education une base solide pour un travail ERP et de gouvernance plus large : elle oblige a se concentrer sur les permissions, l adoption, la qualite des donnees, le reporting et les controles pratiques.'],

  ['Open-source ERP implementation for organizations using Frappe, ERPNext, Odoo, LMS platforms, and education operations systems.', 'Implementation ERP open source pour les organisations utilisant Frappe, ERPNext, Odoo, des plateformes LMS et des systemes d operations educatives.'],
  ['We help organizations implement Frappe, ERPNext, Odoo, LMS platforms, and education operations systems with a practical focus on workflows, data quality, permissions, reporting, and adoption.', 'Nous aidons les organisations a implementer Frappe, ERPNext, Odoo, des plateformes LMS et des systemes d operations educatives avec une attention concrete aux workflows, a la qualite des donnees, aux permissions, au reporting et a l adoption.'],
  ['View all services', 'Voir tous les services'],
  ['Workflow and data discovery', 'Decouverte des workflows et donnees'],
  ['ERP configuration and implementation', 'Configuration et implementation ERP'],
  ['Migration, testing, and adoption', 'Migration, tests et adoption'],
  ['We translate operational processes into ERP structures: records, roles, permissions, approvals, dashboards, reports, and workflows.', 'Nous traduisons les processus operationnels en structures ERP : dossiers, roles, permissions, validations, tableaux de bord, rapports et workflows.'],
  ['We support data migration, UAT, training, go-live preparation, and the practical routines teams need after launch.', 'Nous soutenons la migration des donnees, les tests utilisateurs, la formation, la preparation au go-live et les routines pratiques dont les equipes ont besoin apres le lancement.'],
  ['Why Ifitwala', 'Pourquoi Ifitwala'],
  ['Creators of Ifitwala_Ed', 'Createurs d Ifitwala_Ed'],
  ['Ifitwala is the creator of Ifitwala_Ed, a unified education operations platform built on the Frappe Framework. It brings school operations into one connected system across admissions, student records, family data, learning workflows, staff processes, permissions, reporting, and governance.', 'Ifitwala est le createur d Ifitwala_Ed, une plateforme unifiee d operations educatives construite sur le Framework Frappe. Elle rassemble les operations scolaires dans un systeme connecte couvrant admissions, dossiers eleves, donnees familiales, workflows d apprentissage, processus du personnel, permissions, reporting et gouvernance.'],
  ['We are the creators of Ifitwala_Ed, a unified education operations platform built on the Frappe Framework.', 'Nous sommes les createurs d Ifitwala_Ed, une plateforme unifiee d operations educatives construite sur le Framework Frappe.'],
  ['Our Frappe experience is practical and product-level: modules, workflows, portals, permissions, records, reports, dashboards, and operational processes.', 'Notre experience Frappe est pratique et orientee produit : modules, workflows, portails, permissions, dossiers, rapports, tableaux de bord et processus operationnels.'],
  ['That product experience gives us a strong understanding of how to translate real organizational complexity into structured, usable ERP systems.', 'Cette experience produit nous donne une comprehension solide de la maniere de traduire une vraie complexite organisationnelle en systemes ERP structures et utilisables.'],
  ['Platforms', 'Plateformes'],
  ['We specialize in Frappe Framework, ERPNext, and Frappe-based systems. We also support Odoo implementation projects where organizations need strong workflow mapping, migration planning, permissions design, testing, training, and go-live coordination.', 'Nous sommes specialises dans le Framework Frappe, ERPNext et les systemes bases sur Frappe. Nous accompagnons aussi les projets Odoo lorsque les organisations ont besoin d une cartographie solide des workflows, d une planification de migration, d un design des permissions, de tests, de formation et de coordination du go-live.'],
  ['Frappe Framework custom applications', 'Applications sur mesure Frappe Framework'],
  ['ERPNext implementation', 'Implementation ERPNext'],
  ['Frappe HRMS, CRM, LMS, Helpdesk, and related tools', 'Frappe HRMS, CRM, LMS, Helpdesk et outils associes'],
  ['Odoo implementation support', 'Support d implementation Odoo'],
  ['Moodle implementation and LMS integration', 'Implementation Moodle et integration LMS'],
  ['Ifitwala_Ed for schools and education organizations', 'Ifitwala_Ed pour les ecoles et organisations educatives'],
  ['ERP projects fail when organizations treat them as software installation projects. We focus on the operational layer: what teams do, what data they trust, who is allowed to do what, and how leadership gets reliable visibility.', 'Les projets ERP echouent lorsque les organisations les traitent comme de simples installations logicielles. Nous nous concentrons sur la couche operationnelle : ce que font les equipes, les donnees auxquelles elles font confiance, qui peut faire quoi et comment la direction obtient une visibilite fiable.'],
  ['Workflow mapping and gap analysis', 'Cartographie des workflows et analyse des ecarts'],
  ['Configuration versus customization decisions', 'Decisions entre configuration et personnalisation'],
  ['Master data cleanup and migration planning', 'Nettoyage des donnees de reference et planification de migration'],
  ['Roles, permissions, approvals, and access control', 'Roles, permissions, validations et controle d acces'],
  ['Dashboards, reports, and decision visibility', 'Tableaux de bord, rapports et visibilite decisionnelle'],
  ['UAT, training, go-live, and post-launch support', 'Tests utilisateurs, formation, go-live et support post-lancement'],

  ['A modern education operations platform for institutions that need clarity, structure, and coordinated execution.', 'Une plateforme moderne d operations educatives pour les institutions qui ont besoin de clarte, de structure et d execution coordonnee.'],
  ['See the institution more clearly across academic performance, operations, finance, and cross-team execution.', 'Voir l institution plus clairement a travers la performance academique, les operations, la finance et l execution entre equipes.'],
  ['Replace scattered processes with structured workflows that teams can follow and leadership can trust.', 'Remplacer les processus disperses par des workflows structures que les equipes peuvent suivre et que la direction peut croire.'],
  ['Reduce handoffs, duplicate entry, and fragmented communication between departments.', 'Reduire les transferts manuels, les doubles saisies et la communication fragmentee entre departements.'],
  ['Create a stronger operating foundation for growing schools, districts, and colleges.', 'Creer une base operationnelle plus solide pour les ecoles, reseaux et colleges en croissance.'],
  ['The goal is not to add more software. It is to create a stronger operating system for the institution across the workflows that matter most.', 'L objectif n est pas d ajouter un logiciel de plus. Il est de creer un systeme operationnel plus solide pour l institution dans les workflows qui comptent le plus.'],
  ['Maintain a complete student view across enrollment, attendance, academics, finance, and communication without duplicate entry.', 'Maintenir une vue complete de l eleve a travers inscriptions, presence, academique, finance et communication sans double saisie.'],
  ['Support timetables, coursework, grading, reporting, and academic coordination from one connected platform.', 'Soutenir les emplois du temps, travaux, evaluations, bulletins et coordination academique depuis une plateforme connectee.'],
  ['Track applicants, decisions, onboarding, and transitions with a process that remains visible and structured.', 'Suivre les candidats, decisions, onboarding et transitions avec un processus visible et structure.'],
  ['Bring invoicing, payment tracking, and financial workflows into the same platform used by operational teams.', 'Rassembler facturation, suivi des paiements et workflows financiers dans la meme plateforme que les equipes operationnelles.'],
  ['Reduce manual handoffs between departments with cleaner workflows, ownership, and institutional consistency.', 'Reduire les transferts manuels entre departements grace a des workflows plus clairs, des responsabilites et une coherence institutionnelle.'],
  ['Keep leadership, staff, and families aligned with structured communication and institution-wide reporting.', 'Aligner direction, personnel et familles grace a une communication structuree et un reporting institutionnel.'],
  ['Heads of School and District Leaders', 'Directions d ecole et responsables de reseau'],
  ['Get clearer oversight across academics, operations, finance, and institutional performance.', 'Obtenir une supervision plus claire de l academique, des operations, de la finance et de la performance institutionnelle.'],
  ['Academic Leaders', 'Responsables academiques'],
  ['Coordinate schedules, assessment, reporting, and teaching workflows with less administrative friction.', 'Coordonner les horaires, evaluations, reporting et workflows d enseignement avec moins de friction administrative.'],
  ['Operations Teams', 'Equipes operations'],
  ['Replace scattered tools with one system that keeps records, approvals, and daily processes in sync.', 'Remplacer les outils disperses par un systeme qui garde dossiers, validations et processus quotidiens synchronises.'],
  ['Finance Teams', 'Equipes finance'],
  ['Improve billing accuracy, visibility, and coordination with the rest of the institution.', 'Ameliorer la precision de la facturation, la visibilite et la coordination avec le reste de l institution.'],
  ['IT and Systems Teams', 'Equipes IT et systemes'],
  ['Gain better control over permissions, platform structure, and system ownership without managing disconnected apps.', 'Mieux controler les permissions, la structure de la plateforme et la responsabilite systeme sans gerer des applications deconnectees.'],
  ['Track applicants, admissions decisions, onboarding, and transitions in one visible institutional process.', 'Suivre candidats, decisions d admission, onboarding et transitions dans un processus institutionnel visible.'],
  ['Application tracking', 'Suivi des candidatures'],
  ['Decision workflow', 'Workflow de decision'],
  ['Enrollment readiness', 'Preparation a l inscription'],
  ['Academic Coordination', 'Coordination academique'],
  ['Connect scheduling, academic records, reporting, and classroom workflows to reduce friction for academic teams.', 'Connecter planification, dossiers academiques, reporting et workflows de classe afin de reduire la friction pour les equipes academiques.'],
  ['Timetables and schedules', 'Horaires et emplois du temps'],
  ['Assessment and reporting', 'Evaluation et reporting'],
  ['Academic visibility', 'Visibilite academique'],
  ['Business Office and Operations', 'Bureau administratif et operations'],
  ['Bring billing, operational follow-through, and day-to-day administration into the same platform as the rest of the institution.', 'Amener facturation, suivi operationnel et administration quotidienne dans la meme plateforme que le reste de l institution.'],
  ['Billing and payment flow', 'Flux de facturation et paiements'],
  ['Operational ownership', 'Responsabilite operationnelle'],
  ['Administrative consistency', 'Coherence administrative'],
  ['Support a more coordinated experience for leadership, staff, families, and institution reporting needs.', 'Soutenir une experience plus coordonnee pour la direction, le personnel, les familles et les besoins de reporting institutionnel.'],
  ['Structured communication', 'Communication structuree'],
  ['Leadership reporting', 'Reporting de direction'],
  ['Cross-team alignment', 'Alignement entre equipes'],
  ['Book a tailored walkthrough focused on the workflows your leadership, academic, operations, finance, or technology teams need to review.', 'Reservez une demonstration adaptee aux workflows que vos equipes de direction, academiques, operations, finance ou technologie doivent evaluer.'],

  ['Map the institution structure, teams, workflows, and reporting needs that matter to leadership.', 'Cartographier la structure de l institution, les equipes, les workflows et les besoins de reporting importants pour la direction.'],
  ['Set up records, permissions, operational flows, and the data model required for a confident rollout.', 'Configurer les dossiers, permissions, flux operationnels et le modele de donnees necessaires a un deploiement fiable.'],
  ['Launch with training, guided change management, and the workflows your teams need first.', 'Lancer avec formation, accompagnement du changement et les workflows dont vos equipes ont besoin en premier.'],
  ['Start with institutional structure', 'Commencer par la structure institutionnelle'],
  ['A credible rollout begins with the institution model, teams, permissions, and workflows that matter most.', 'Un deploiement credible commence par le modele institutionnel, les equipes, les permissions et les workflows essentiels.'],
  ['Sequence adoption intentionally', 'Sequencer l adoption intentionnellement'],
  ['Launch the right workflows first so early usage builds confidence instead of confusion.', 'Lancer les bons workflows en premier afin que les premiers usages creent de la confiance plutot que de la confusion.'],
  ['Align teams around ownership', 'Aligner les equipes autour des responsabilites'],
  ['Implementation works better when leadership, academics, operations, and technical stakeholders know their roles.', 'L implementation fonctionne mieux lorsque direction, academique, operations et parties prenantes techniques connaissent leurs roles.'],
  ['Train around real work', 'Former autour du travail reel'],
  ['Adoption improves when training is tied to actual institutional tasks rather than abstract software tours.', 'L adoption progresse lorsque la formation est liee aux taches institutionnelles reelles plutot qu a des visites abstraites du logiciel.'],
  ['Leadership sponsor', 'Sponsor de direction'],
  ['Sets priorities, success criteria, and the institutional context for the rollout.', 'Definit les priorites, criteres de succes et contexte institutionnel du deploiement.'],
  ['Academic lead', 'Referent academique'],
  ['Represents schedules, grading, reporting, and academic coordination requirements.', 'Represente les besoins d horaires, evaluation, reporting et coordination academique.'],
  ['Operations lead', 'Referent operations'],
  ['Owns the day-to-day workflows that need to stay consistent during migration and launch.', 'Porte les workflows quotidiens qui doivent rester coherents pendant la migration et le lancement.'],
  ['Finance or business office lead', 'Referent finance ou bureau administratif'],
  ['Ensures billing, collections, and finance-related processes fit the institution’s operating reality.', 'S assure que la facturation, les encaissements et les processus financiers correspondent a la realite operationnelle de l institution.'],
  ['IT or systems lead', 'Referent IT ou systemes'],
  ['Reviews permissions, data structure, environment ownership, and operational controls.', 'Revoit les permissions, la structure des donnees, la responsabilite des environnements et les controles operationnels.'],
  ['A clearer institution data model', 'Un modele de donnees institutionnel plus clair'],
  ['Stronger permissions and team ownership', 'Des permissions et responsabilites d equipe plus solides'],
  ['More consistent workflows across departments', 'Des workflows plus coherents entre departements'],
  ['A rollout path leadership can explain with confidence', 'Un chemin de deploiement que la direction peut expliquer avec confiance'],
  ['Use the demo process to review not only product breadth, but also how the rollout would be sequenced, who should participate, and what institutional ownership looks like after launch.', 'Utiliser le processus de demo pour revoir non seulement la couverture produit, mais aussi la sequence de deploiement, les participants necessaires et l appropriation institutionnelle apres lancement.'],
  ['Book a walkthrough and use it to discuss structure, permissions, migration readiness, and the first workflows your teams would need live.', 'Reservez une demonstration pour discuter structure, permissions, preparation de migration et premiers workflows a mettre en production.'],

  ['Trust in education software is not only about features. It is about operational discipline.', 'La confiance dans un logiciel educatif ne concerne pas seulement les fonctionnalites. Elle concerne la discipline operationnelle.'],
  ['A strong evaluation covers permissions, continuity, ownership, and support before rollout begins.', 'Une evaluation solide couvre les permissions, la continuite, les responsabilites et le support avant le debut du deploiement.'],
  ['Use the sales process to review the areas that matter most to your institution’s governance model.', 'Utilisez le processus commercial pour revoir les domaines les plus importants pour le modele de gouvernance de votre institution.'],
  ['Access and Permissions', 'Acces et permissions'],
  ['Institutional teams should be able to evaluate how access is structured, segmented, and governed across roles.', 'Les equipes institutionnelles doivent pouvoir evaluer comment l acces est structure, segmente et gouverne entre les roles.'],
  ['Data Handling and Ownership', 'Gestion et responsabilite des donnees'],
  ['Buyers should understand where data lives, how it is managed, and what operational responsibilities sit with the platform and the institution.', 'Les acheteurs doivent comprendre ou vivent les donnees, comment elles sont gerees et quelles responsabilites operationnelles appartiennent a la plateforme et a l institution.'],
  ['Operational Continuity', 'Continuite operationnelle'],
  ['The trust discussion should cover backups, recovery expectations, maintenance discipline, and resilience planning.', 'La discussion de confiance doit couvrir les sauvegardes, les attentes de reprise, la discipline de maintenance et la planification de resilience.'],
  ['Support and Accountability', 'Support et redevabilite'],
  ['Institutions need a clear path for issue ownership, escalation, and day-to-day operational support.', 'Les institutions ont besoin d un chemin clair pour la responsabilite des incidents, l escalade et le support operationnel quotidien.'],
  ['Role-based access and who can see or change sensitive information', 'Acces par role et personnes pouvant voir ou modifier les informations sensibles'],
  ['How records, operational actions, and reporting can be reviewed or audited', 'Comment les dossiers, actions operationnelles et rapports peuvent etre revus ou audites'],
  ['Backup and recovery expectations appropriate to institutional operations', 'Attentes de sauvegarde et reprise adaptees aux operations institutionnelles'],
  ['Who owns environment, configuration, and operational changes', 'Qui porte l environnement, la configuration et les changements operationnels'],
  ['What the support and escalation path looks like during live usage', 'A quoi ressemble le support et l escalade pendant l usage en production'],
  ['How implementation and change management reduce avoidable risk', 'Comment l implementation et la gestion du changement reduisent les risques evitables'],
  ['Ask direct questions about how access is governed, how institutional ownership is handled, and what the support path looks like when workflows are live.', 'Posez des questions directes sur la gouvernance des acces, la responsabilite institutionnelle et le chemin de support lorsque les workflows sont en production.'],
  ['Review not only what the product can do, but also how the platform would fit your institution’s operating model, governance expectations, and rollout discipline.', 'Revoyez non seulement ce que le produit peut faire, mais aussi comment la plateforme s integre a votre modele operationnel, vos attentes de gouvernance et votre discipline de deploiement.'],
  ['Trust is strongest when the conversation is clear about responsibilities, escalation, continuity, and the practical realities of daily institutional use.', 'La confiance est plus forte lorsque la discussion est claire sur les responsabilites, l escalade, la continuite et les realites pratiques de l usage quotidien.'],
  ['This page intentionally frames the trust discussion areas institutions should review. Product-specific operating details should be confirmed during your evaluation process.', 'Cette page cadre volontairement les domaines de confiance que les institutions devraient revoir. Les details operationnels propres au produit doivent etre confirmes pendant votre evaluation.'],
  ['Use the demo to review the areas that matter most to your institution’s governance, operational continuity, and support model.', 'Utilisez la demo pour revoir les domaines les plus importants pour la gouvernance, la continuite operationnelle et le modele de support de votre institution.'],
  ['Review implementation', 'Revoir l implementation'],
]

function walkHtmlFiles(root) {
  const out = []
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    if (entry.name.startsWith('_') || locales.includes(entry.name)) {
      continue
    }
    const fullPath = path.join(root, entry.name)
    if (entry.isDirectory()) {
      out.push(...walkHtmlFiles(fullPath))
    } else if (entry.isFile() && entry.name === 'index.html') {
      out.push(fullPath)
    }
  }
  return out
}

function routeForFile(file) {
  const relative = path.relative(distRoot, file)
  if (relative === 'index.html') {
    return '/'
  }
  return `/${path.dirname(relative).replace(/\\/g, '/')}/`
}

function shouldLocalize(route) {
  if (route.startsWith('/docs/')) {
    return false
  }
  const first = route.split('/').filter(Boolean)[0] || ''
  return mainRoutePrefixes.has(first)
}

function ensureDir(file) {
  fs.mkdirSync(path.dirname(file), { recursive: true })
}

function destinationFor(route, locale) {
  const trimmed = route.replace(/^\/+|\/+$/g, '')
  return trimmed
    ? path.join(distRoot, locale, trimmed, 'index.html')
    : path.join(distRoot, locale, 'index.html')
}

function replaceAll(input, from, to) {
  return input.split(from).join(to)
}

function translateToFrench(html, route) {
  let out = html
    .replace(/<html lang="en"/g, '<html lang="fr"')
    .replace(/(<link rel="canonical" href="https:\/\/ifitwala\.com\/)en(\/[^"]*")/g, '$1fr$2')
    .replace(/href="\/en\//g, 'href="/fr/')
    .replace(/href="\/en"/g, 'href="/fr"')

  const orderedReplacements = [...replacements].sort((a, b) => b[0].length - a[0].length)
  for (const [from, to] of orderedReplacements) {
    out = replaceAll(out, from, to)
  }

  const currentPath = route === '/' ? '/' : route
  const escapedPath = currentPath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const targetPath = escapedPath === '\\/' ? '/' : escapedPath
  out = out.replace(
    new RegExp(`href="/fr${targetPath}"([^>]*>\\s*EN\\s*</a>)`, 'g'),
    `href="/en${currentPath}"$1`
  )
  out = out.replace(/aria-current="page"([^>]*>\s*EN\s*<\/a>)/g, '$1')
  out = out.replace(
    new RegExp(`(<a href="/fr${targetPath}" class="[^"]*?)hover:bg-moss/40 hover:text-canopy([^"]*">\\s*FR\\s*</a>)`, 'g'),
    '$1bg-canopy text-white$2'
  )
  out = out.replace(
    new RegExp(`(<a href="/en${targetPath}" class="[^"]*?)bg-canopy text-white([^"]*"[^>]*>\\s*EN\\s*</a>)`, 'g'),
    '$1hover:bg-moss/40 hover:text-canopy$2'
  )

  const enAbsolute = `https://ifitwala.com/en${currentPath}`
  const frAbsolute = `https://ifitwala.com/fr${currentPath}`
  out = out.split(enAbsolute).join(frAbsolute)
  out = out
    .replace(
      new RegExp(`(<link rel="alternate" hreflang="en" href=")${escapeRegExp(frAbsolute)}(")`, 'g'),
      `$1${enAbsolute}$2`
    )
    .replace(
      new RegExp(`(<link rel="alternate" hreflang="x-default" href=")${escapeRegExp(frAbsolute)}(")`, 'g'),
      `$1${enAbsolute}$2`
    )
    .replace(/"inLanguage":"en"/g, '"inLanguage":"fr"')

  return out
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function copyLocalizedPage(source, route) {
  const html = fs.readFileSync(source, 'utf8')
  const enTarget = destinationFor(route, 'en')
  const frTarget = destinationFor(route, 'fr')
  ensureDir(enTarget)
  ensureDir(frTarget)
  fs.writeFileSync(enTarget, html, 'utf8')
  fs.writeFileSync(frTarget, translateToFrench(html, route), 'utf8')
}

if (!fs.existsSync(distRoot)) {
  throw new Error(`Missing Astro output directory: ${distRoot}`)
}

const htmlFiles = walkHtmlFiles(distRoot).filter((file) => shouldLocalize(routeForFile(file)))
for (const file of htmlFiles) {
  copyLocalizedPage(file, routeForFile(file))
}

console.log(`[i18n] generated ${htmlFiles.length * 2} localized HTML pages under /en and /fr`)
