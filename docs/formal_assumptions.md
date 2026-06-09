# Formal Assumptions

This document states the working assumptions used by the reinterpretive creativity model.

These assumptions are limited to the current artificial graph model. They are not claims about creativity in general.

## 1. World models

A world model is represented as a signed directed graph.

- Nodes are abstract elements.
- Directed edges are relations between elements.
- Edge signs are positive or negative relation labels.

The graph is a modeling device. It is not a full semantic theory of cognition.

## 2. Inconsistency

An inconsistency is a structural conflict inside a world model.

In the current implementation, inconsistency is represented by incompatible signed relations in the graph.

Inconsistency is not a creative act. It only defines a condition under which repair or reinterpretation may be attempted.

## 3. Repair

Repair is an operation that reduces inconsistency while staying close to the starting model.

Local repair is expected to preserve much of the original structure.

Repair can be useful and may outperform reinterpretation under some conditions.

## 4. Reinterpretation

Reinterpretation is a search for an alternative model that is coherent, different from the starting model, and evaluated by structural proxy measures.

A reinterpretation is not merely any change. It must be assessed against repair and other baselines.

The model does not assume that reinterpretation is always preferable.

## 5. Score components

The current score is treated as a structural proxy composed of measurable components.

The relevant components are:

- distance from a reference or teacher model,
- preservation of the starting model,
- utility proxy,
- aggregate score.

These components are diagnostic measurements, not human value judgments.

## 6. Outcomes

A trial can be interpreted as success, failure, or neutral only relative to specified baselines and metrics.

Success means that reinterpretation outperforms relevant baselines under the defined score.

Failure means that a baseline such as local repair, random search, or another method outperforms reinterpretation.

Neutral means that the observed difference is absent, small, or unstable under the current measurement setup.

## 7. Falsification conditions

The model is weakened if reinterpretation fails to outperform baselines across the conditions where it is expected to help.

The model is also weakened if apparent wins are explained entirely by score artifacts, teacher-model bias, candidate-limit effects, or random seed sensitivity.

A useful model must identify both winning and losing conditions.

## 8. Non-goals

This project does not aim to prove creativity itself.

It does not claim that errors are creative, that inconsistency causes creativity, or that utility proxy captures human value.

It only studies limited structural relations among inconsistent world models, repair, reinterpretation, and diagnostic scores.
