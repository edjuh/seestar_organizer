# 🗺️ S30-PRO Development Roadmap: The Rommeldam Epic

This document outlines the architectural journey of the S30-PRO autonomous observatory, structurally mapped to the characters and society of Marten Toonder's *Tom Poes / Heer Bommel* universe.

## ✅ Past Milestones (The Foundation)
* **v0.0 Beunhaas:** Environment Validation.
* **v0.1 Brigadier Snuf:** The State Engine.
* **v0.2 Zedekia Zwederkoorn:** The Alpaca Bridge Patch.
* **v0.3 Joris Goedbloed:** Target Acquisition.
* **v0.4 Zachtzalver:** Command Translation.
* **v0.5 Hiep Hieper:** The Orchestrator (The Golden Bridge).
* **v0.6 Insp. Priembickel:** Hardening and Git strictness.
* **v0.7 Argus :** The all-seeing autonomous observer.
* **v0.8 Lieven Brekel:** Mid-sequence weather aborts and WCS bridge hardening.
* **v0.9 Terpen Tijn (Current):** "Het is prut!" The Aperture Grip. Sub-pixel centroiding, dynamic CFA debayering/fallback, and offline AAVSO Zero-Point calibration.
## 🚀 Near-Term Milestones (The Specialists)
* **v1.0 Kwetal:** Converting the Orchestrator into a bulletproof `systemd` background daemon.
* **v1.1 Pee Pastinakel:** Dynamic aperture scaling (PSF fitting) and saturation detection to handle bright-star magnitude offsets.

# 🗺️ S30-PRO Development Roadmap: The Rommeldam Epic

This document outlines the architectural journey of the S30-PRO autonomous observatory, structurally mapped to the characters of Marten Toonder's universe.

## ✅ Past Milestones (The Foundation)
* **v0.0 Beunhaas:** Environment Validation.
* **v0.1 Brigadier Snuf:** The State Engine.
* **v0.2 Zedekia Zwederkoorn:** The Alpaca Bridge Patch.
* **v0.3 Joris Goedbloed:** Target Acquisition.
* **v0.4 Zachtzalver:** Command Translation.
* **v0.5 Hiep Hieper:** The Orchestrator (The Golden Bridge).
* **v0.6 Insp. Priembickel:** Hardening and Git strictness.
* **v0.7 Argus:** The all-seeing autonomous observer.
* **v0.8 Lieven Brekel:** Mid-sequence weather aborts and WCS bridge hardening.
* **v0.9 Terpen Tijn (CURRENT):** "Het is prut!" Westward priority active. Sub-pixel centroiding, dynamic CFA debayering, and stable Alpaca handshake for AAVSO targets.

## 🚀 Near-Term Milestones (The Specialists)
* **v1.0 Kwetal:** Converting the Orchestrator into a bulletproof `systemd` background daemon.
* **v1.1 Pee Pastinakel:** Dynamic aperture scaling (PSF fitting) and saturation detection.

---

## 🌲 Epoch 1: Het Kleine Volkje (v1.x)
*The invisible, tireless workers in the background. Focuses on system resilience and background magic.*
* **v1.0 Kwetal:** Converting the Orchestrator into a bulletproof `systemd` background daemon.
* **v1.1 Pee Pastinakel:** "Talks to the plants" (environmental sensor tuning).
* **v1.2 Garmt:** A down-to-earth, stable baseline update.
* **v1.3 Monkel:** *"Een mens kan ook nooit eens rustig..."* Fixing daemon interruption bugs.
* **v1.4 Kriel:** A small, agile performance update.
* **v1.5 Humpie:** A small, targeted interface/CLI fix.
* **v1.6 Jochem:** Giving the background workers a bigger role.
* **v1.7 Oene:** Short, strong, and highly optimized code refactoring.
* **v1.8 Snotolf:** An authentic, slightly spicy underlying system change.
* **v1.9 Fliep:** The fast, final wrap-up version.

---

## ☕ Epoch 2: The Women of Rommeldam (v2.x)
*The caretakers and organizers. Focuses on bringing order, analysis, and presentation to the raw data.*
* **v2.0 Anne Marie Doddel:** Real-time photometric analysis and beautiful AAVSO light-curves.
* **v2.1 Anne-Miebetje:** The classic first sub-version refinement.
* **v2.2 Wobbe:** A highly stable, technical build.
* **v2.3 Wolle:** Dedicated to visual graph and plot updates.
* **v2.4 Irma:** *(Irma de vlieg)* That one tiny, annoying bug fix.
* **v2.5 Prettig:** A major UX and ease-of-use improvement.
* **v2.6 Zonnetje:** An optimistic feature-release.
* **v2.7 Agatha:** *(Vrouw Dickerdack)* A more "official" or business-grade build.
* **v2.8 Georgette:** *(Vrouw Grootgrut)* Heavy focus on new data integration.
* **v2.9 Tante Pollewop:** The final loving polish.

---

## 🧠 Epoch 3: De Medici & Analisten (v3.x)
*Focuses on the "health," logic, and psychological stability of the code.*
* **v3.0 Zielknijper:** The basis for the psychological stability of the code.
* **v3.1 Galzalver:** Plasters for the small wounds (hotfixes).
* **v3.2 Dr. Plus:** Added value and positive data-processing results.
* **v3.3 Alexander Pieps:** Refined data analysis down to the square millimeter.
* **v3.4 Sickbock:** Boundary-pushing (and risky) experimental features.
* **v3.5 Okke Zielzoeker:** Deep-diving into user analytics.
* **v3.6 Dr. Baboen:** Solid medical support under the hood.

---

## 🏛️ Epoch 4: De Bureaucratie & Middenstand (v4.x)
*Focuses on rules, administration, and AAVSO compliance.*
* **v4.0 Ambtenaar Dorknoper:** *"Dat is buiten de voorschriften."* Strict AAVSO compliance, immutable audit logs, and official submissions.
* **v4.1 Bulle Bas:** Enforcement of security and protocols.
* **v4.2 Notaris Canteclaer:** The fine print and legally correct handling.
* **v4.3 Dickerdack:** The mayor keeping the entire pipeline running smoothly.
* **v4.4 Grootgrut:** Inventory management and database handling.
* **v4.5 Pastuiven Verkwansel:** The secretary keeping the file systems ordered.
* **v4.6 Ambtenaar Plof:** Heavy lifting for massive datasets.
* **v4.7 Referendaris Lapsnuut:** The administrative finishing touch.

---

## 🍷 Epoch 5: De Adel & De Kleine Club (v5.x)
*Focuses on high-society UI/UX and elite processing. "Een release voor luyden van stand."*
* **v5.0 Markies de Canteclaer:** The place of honor. A GUI so refined the rabble won't understand it.
* **v5.1 Graaf van Zandbergen:** A solid, noble UI foundation.
* **v5.2 Baron de l'Esprit:** Refined, intellectual algorithms.
* **v5.3 Jonker Wip:** A light-footed, snappy UI update.
* **v5.4 Oud-majoor Buitenzorg:** Background discipline and memory management.
* **v5.6 De heer Steinhacker:** Industrial-grade optimizations for heavy capital logic.
* **v5.8 Notaris Fijn van Draad:** The perfect aristocratic administrative closure.

---

## 🔮 Epoch 6: Het Magische Bos (v6.x)
*Focuses on complex, inexplicable, and esoteric software forces.*
* **v6.0 Hocus Pas:** Where the true magic happens (machine learning/AI integration).
* **v6.1 Zwarte Zwadderneel:** Edge-cases and error handling. *Log requirement: System must state "Deze update is gedoemd te mislukken" on startup.*
* **v6.2 De Zwarte Raaf:** Mysterious, lightning-fast data transfer protocols.
* **v6.3 Oene de Reus:** Brute-forcing massive chunks of unstructured data.
* **v6.4 Argus de Draak:** Guarding the treasure room (advanced encryption/security).
* **v6.5 De Gnoom:** Deep, hidden underground scripts.
* **v6.6 De Heks van de Nevelvallei:** Advanced image filters peering through fog/clouds.
* **v6.7 Magister Morya:** Esoteric and highly abstract functions.

---

## 🔬 Epoch 7: De Wetenschappers & Fenomenologen (v7.x)
*Focuses on heavy mathematics, deep astrophysics, and phenomena.*
* **v7.0 Professor Prlwytzkofsky:** Phenomenological consistency of the night sky. *Log requirement: All fatal exceptions must be rendered in phonetic Polish ("Praw!").*
* **v7.4 Joachim Snerle:** Detecting "earthly" influences (atmospheric refraction compensation).

---

## 💰 Epoch 8: De Zware Jongens & De Handel (v8.x)
*Focuses on pure efficiency and data brokering. "Geld moet rollen!"*
* **v8.0 Bul Super:** The Boss. "Zaken zijn zaken." *Requirement: Bug reports only accepted if accompanied by a "commission."*
* **v8.1 Knol:** The muscle. Smashing through database bottlenecks.
* **v8.2 De Markelaar:** The broker. External API connections and data trading.
* **v8.3 De Lorreman:** Garbage collection and archiving. *Note: "Geen bug is te klein voor de handel."*
* **v8.5 O. Fanth Mzn:** The media magnate. Publishing and exporting final results to the web.
* **v8.6 Super-Hieper Transit:** Lightning-fast internal logistics and bus transfers.
* **v8.7 De Kassier:** The final financial and administrative wrap-up.
