# Experimental Reasoning

This project is as much about *how to narrow a scientific claim* as it is about any particular neural architecture.

## Accessibility versus use

Suppose a hidden state is followed by a native consumer that performs poorly on a task. Poor output alone does not tell us where the failure occurred.

At least two explanations remain:

1. **Representation failure:** the state no longer exposes the relevant distinction to the consumer family we care about.
2. **Utilization failure:** the distinction remains accessible, but the native consumer fails to exploit it.

A frozen-state probe helps separate these explanations. If a deliberately small probe generalizes well while the native consumer does not, representation destruction becomes a less economical explanation for that particular recoverable signal.

This still does not prove causal use. A separately trained probe is a new consumer, and it may use information the native model ignores.

### Understanding questions

**Why freeze the state before fitting the probe?**  
To prevent improved decoding from being explained by the representation adapting to the diagnostic task.

**Why start with a small probe family?**  
Because success with a restricted decoder gives a simpler accessibility result and reduces alternative explanations based on decoder expressivity.

**Why isn't probe success enough to establish causal use?**  
Because accessibility to a new decoder does not show that the original downstream computation depends on the decoded feature.

## Controls as attacks on explanations

A useful way to design controls is to ask: *If my preferred interpretation were false, what mundane mechanism could still produce this result?*

For a probe result, examples include target leakage, train/evaluation dependence, excessive classifier capacity, coordinate artifacts, or a generally overpowered analysis pipeline. Label shuffles, representation shuffles, matched random features, grouped splits, and alternate coordinate treatments attack different alternatives.

Controls are therefore not ceremonial additions after the experiment. They are part of the argument.

## Bounded negative results

A failed diagnostic rarely proves that information is absent in an unrestricted sense.

If an affine probe fails under a valid protocol, the defensible claim is approximately:

> this target was not recoverable by the tested affine probe family under the stated data and evaluation conditions.

That is narrower than:

> the representation contains no information about the target.

The distinction matters because a nonlinear decoder, a different amount of data, or another operational definition of the target may behave differently.

### Understanding questions

**Why is “the linear probe failed” not equivalent to “the information is gone”?**  
Because probe failure is relative to the decoder family, data, optimization, and protocol.

**What makes a negative result scientifically useful?**  
A well-specified boundary: it eliminates a particular hypothesis or mechanism without pretending to eliminate stronger possibilities that were never tested.

## The next-experiment principle

A good experiment should change what experiment is rational to run next.

If evidence favors representation failure, invest in representation or training interventions. If evidence favors underutilization, first test small downstream repairs while leaving the representation fixed. This avoids changing many components before locating the bottleneck.

The research notes emphasize these belief updates because they expose the reasoning connecting milestones rather than presenting results as an isolated scoreboard.
