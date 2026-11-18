# Article dependencies and notebook identity

The `depends_on` field names conceptual prerequisites. It does not encode every
background citation or the next article in publication order. A root means no
prerequisite is declared within this collection; it does not mean the argument
has no intellectual antecedents.

The November 10 audience review checked the complete published argument against
the metadata. The original 13 milestone relationships are:

| Milestone | Prerequisite | Reason |
| --- | --- | --- |
| 001 | None | Introduces the representation-versus-computation question. |
| 002 | 001 | Decomposes the spectral performance gap introduced in 001. This missing edge is now declared. |
| 003 | 002 | Holds the uncombined state fixed after the stage comparison exposes pre-composition loss. |
| 004 | 003 | Ablates the polar-native block whose gain was isolated in 003. |
| 005 | 004 | Keeps the isolated attention mechanism fixed while comparing recurrent-state constructions. |
| 006 | 005 | Revisits the frozen endpoint using trajectories, regularization controls, and checkpoint selection. |
| 007 | 005 | Derives properties needed to evaluate explanations of the unit constraint. It is a parallel branch to 006. |
| 008 | 007 | Turns local normalization properties into frozen-model mechanism tests. |
| 009 | 007 | Generalizes the derive-before-training method into explicit claim types and a theorem ledger. |
| 010 | None | Starts the recurrence-compatible equivalence question from translation and task sufficiency. Chronological proximity to 009 is not a prerequisite. |
| 011 | 010 | Uses task-preserving equivalence and invariance to choose geometric constructions. |
| 012 | 010 | Makes future distinctions observable in revision-history data. Earlier model diagnostics and the source-unit correction are background; the article explains those locally. |
| 013 | 012 | Uses the frozen revision-branch task to distinguish recoverability from native use. The article supplies its tangent-space definitions and links formal/background evidence directly. |

The later work-in-progress article, “Can a small consumer use what the state
knows?”, declares 013 as its prerequisite because it asks the next question
raised by that result. The packaging and interruption essays explain their own
starting concepts and remain separate roots. They are not milestones 014–016.

Each numbered article now declares `milestone` and `source_notebook` explicitly.
The latter is the basename of the primary preserved notebook, without `.ipynb`.
It records the relationship already stated in the article's sources; it does
not associate every referenced background notebook as the primary record.
Neither this metadata nor reader navigation changes notebook bytes.
