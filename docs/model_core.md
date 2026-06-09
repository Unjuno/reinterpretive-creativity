# Model Core

This project studies a limited model of reinterpretive creativity.

It does not claim to explain creativity in general. It models cases where an internally inconsistent world model can be transformed into a coherent, different, and structurally valuable alternative model.

## Target

The target phenomenon is reinterpretation of an inconsistent world model.

The project focuses on artificial signed directed graphs, not full human cognition.

## World model

A world model is represented as a signed directed graph.

- Nodes represent elements in the model.
- Directed edges represent relations between elements.
- Edge signs represent positive or negative relations.

## Internal inconsistency

An inconsistency is a structural conflict inside the model, such as incompatible positive and negative relations.

Inconsistency is not treated as creativity itself. It is only a possible trigger for reinterpretation search.

## Repair

Repair is an operation that reduces inconsistency.

Local repair may improve consistency while preserving most of the original structure.

## Reinterpretation

Reinterpretation is treated as a search for an alternative model that is:

- more coherent than the inconsistent starting model,
- structurally different from the starting model,
- evaluated by structural proxy measures.

Reinterpretation is not assumed to be better than repair in all cases.

## Value proxy

The utility proxy is a structural measurement proxy.

It is not a model of human value judgment.

## Success condition

A reinterpretation result is successful only in the limited experimental sense when it scores better than relevant baselines under the defined structural metrics.

## Failure condition

The model should also identify cases where reinterpretation search loses to local repair, random search, or other baselines.

These failures are part of the model, not exceptions to hide.

## Non-claims

This project does not claim that:

- errors are creative,
- inconsistency causes creativity,
- reinterpretation is always best,
- utility proxy captures human value,
- formal proofs prove creativity itself.

The project only studies limited structural relations among definitions, simulations, and diagnostic measurements.
