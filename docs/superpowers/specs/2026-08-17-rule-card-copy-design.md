# Rule Card Copy Design

## Goal

Make the four demo rule cards communicate the policy-blindness contrast without changing their presentation or interaction.

## Scope

Only text inside the existing Agent and Owner faces of the four cards in `index.html` changes. Card titles, order, markup structure, CSS classes, links, buttons, and flip behavior remain as they are.

## Copy Rules

- Every Agent face presents a simple task followed by an outcome-only decline using the pattern `DECLINED — no reason given`.
- Rule 02 and Rule 04 retain their preceding successful payment counts, but both end with the same outcome-only decline phrase.
- Every Owner face names exactly the relevant private policy reason in plain language.
- The shared policy values are: $0.15 maximum per payment, $0.35 rolling budget per hour, four payments per hour, and approved vendors only.
- Rule 02 identifies cumulative spend: a fourth $0.10 payment would make the total $0.40, over the $0.35 budget.
- Rule 04 identifies request count: a fifth request exceeds the four-payments-per-hour rate limit, independent of the budget rule.
- Implementation details such as ports, endpoint paths, URLs, and rule identifiers are removed from these cards.

## Verification

Run the landing-page validator, then inspect the `index.html` diff to confirm that only the card body copy changed.
