# [Syn-QA²: Evaluating False Assumptions in Long-tail Questions with Synthetic QA Datasets](http://arxiv.org/abs/2403.12145)

## About
"Sensitivity to false assumptions (or false premises) in information-seeking questions is critical for robust question-answering (QA) systems. Recent work has shown that false assumptions in naturally occurring questions pose challenges to current models with low performance on both generative QA and simple detection tasks. However, the focus of existing work on naturally occurring questions leads to a gap in the analysis of model behavior on the long tail of the distribution of possible questions. 

To this end, we introduce Syn-(QA)², a set of two synthetically generated QA datasets: one generated using perturbed relations from Wikidata and the other by perturbing HotpotQA. Our findings from evaluating a range of large language models are threefold: 
- false assumptions in QA are challenging, echoing the findings of prior work;
- the binary detection task is challenging even compared to the difficulty of generative QA itself, possibly due to the linguistic structure of the problem; and
- the detection task is more challenging with long-tail questions compared to naturally occurring questions, highlighting the utility of our synthetic datasets and generation method."

## Dataset 
[Download the Syn-QA² Dataset](https://drive.google.com/file/d/1kPq-V-khBqkA1lUGg1CSdYFtpeUyoS6d/view?usp=sharing)  
Password: `synqa2`

The dataset contains 1,812 question pairs, divided into 1,165 single-hop and 647 multi-hop questions. Each pair contrasts a question with a false assumption against a counterpart without, aimed at testing QA systems' ability to identify and handle false presuppositions.


## Evaluation Framework
Evaluations were performed on models including GPT-4, GPT-3.5, Llama-2-70B, PaLM-2, and Flan-T5-XXL using various approaches:
- Zero-shot
- Few-shot
- Few-shot with chain-of-thought reasoning

Explore the comprehensive findings in our [paper](http://arxiv.org/abs/2403.12145).

## Cite This Work
```bibtex
@article{acl2024synqa2,
  title={Syn-QA2: Evaluating False Assumptions in Long-tail Questions with Synthetic QA Datasets},
  author={Daswani, A., Sawant, R., & Kim, N.},
  journal={ArXiv},
  year={2024},
  eprint={2403.12145}
}
```


