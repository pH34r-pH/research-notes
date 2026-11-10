---
title: "Can a small consumer use what the state knows?"
description: "An open question about turning information in a frozen model state into better next-byte predictions."
short_title: "Can a small consumer use what the state knows?"
date: 2026-11-01
article_kind: work-in-progress
depends_on: [accessible-does-not-imply-used]
authors:
  - name: Tyler J.H.G.
tags:
  - research in progress
---

# Can a small consumer use what the state knows?

**Work in progress:** This article presents an open question; no new result is reported.

In the [last article](https://tyharbin.com/articles/accessible-does-not-imply-used/), I found that a small probe could recover a particular distinction from a frozen model state, even though the model's own consumer barely used that distinction on the same benchmark. The obvious next question is whether I can change the consumer and get better predictions out of the information that's already there.

The probe result doesn't automatically answer that question, because the probe and the model aren't doing exactly the same task. The probe distinguishes a particular pair of outcomes; the model has to assign probabilities across all 256 possible next-byte values. Being able to tell two situations apart is useful, but it doesn't necessarily tell us which byte should come next.

For example, suppose a state has enough information to tell whether the next byte is likely to be a letter or punctuation. A probe could be very good at recovering that distinction, but if it can't help distinguish between the possible letters, then it might not improve the full next-byte prediction very much. So the question is not just whether the state carries a signal; it's whether a small consumer can use that signal to improve the actual prediction task.


```{figure} ./small-consumer.svg
:alt: A frozen state feeds both the original consumer and a candidate readout, which are compared on the same held-out task.

A frozen state feeds both the original consumer and a candidate readout, which are compared on the same held-out task.
```

## Hold the state fixed

The first thing I want to do is keep the state-producing model frozen and compare its original consumer with small alternative readouts. If I change the state and the consumer at the same time, then an improvement could be due to either change, or an interaction between them. Holding the representation fixed gives the consumer a more direct test.

A natural starting point is an affine readout: multiply the existing state by a learned matrix, add a bias, and turn the resulting scores into a probability distribution over the next byte. This is similar in spirit to the earlier probe, but it is trained and evaluated on the full prediction task, rather than on the narrower branch distinction.

If the new readout improves held-out predictions, that would show that this consumer can use the frozen state more effectively under the test. It wouldn't by itself show that the original consumer was using the same signal, or tell us which part of the state caused the improvement. Those would need additional interventions.

On the other hand, if the readout doesn't improve predictions, that doesn't mean there is no useful information in the state. The branch distinction may not be sufficient to improve the full byte distribution, the readout may be too limited, or the test may not have enough evidence to separate those possibilities. A negative result would have to be interpreted within the consumer family and evaluation procedure that were actually tested.

## What am I measuring?

The comparison needs to use held-out examples and the same evaluation procedure for the original and replacement consumers. The primary result should be next-byte prediction performance, not the branch-probe score. It also needs controls that challenge alternatives such as leakage or a relationship between states and labels that doesn't survive when the relevant structure is disturbed.

This is a fairly narrow question, and I want to keep it that way. A positive result on this model and task wouldn't establish that every model has a readout problem; a negative result wouldn't prove that no larger or different consumer could use the information. Either result could still change what I try next.

The public chronology identifies this as the next experiment, but holds the next numbered milestone until the result and interpretation are stable. There is no new result to report here. For now, the question is: how much of the information the probe recovered can a small consumer turn into better next-byte predictions?

**Sources:** [Milestone 013](https://tyharbin.com/articles/accessible-does-not-imply-used/); [public chronology](https://github.com/pH34r-pH/research-notes/blob/3609bb076195036ace30e2dcbc7eb62353bcbfb4/CHRONOLOGY.md); [representation and readout](https://github.com/pH34r-pH/research-notes/blob/3609bb076195036ace30e2dcbc7eb62353bcbfb4/reference/representation-and-readout.md).
