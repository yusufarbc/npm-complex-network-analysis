#literature review

-------

## 1-The web of dependencies a complex network analysis of the NPM
abstract
Open-source software development is a collaborative effort resulting in complex dependencies
between software packages. Unlike proprietary software, the open-source model offers a unique
opportunity to analyse and trace these dependencies due to its public availability. This thesis
maps out the complex dependency network within the npm ecosystem, the package manager
for JavaScript. JavaScript is the world’s most widely used programming language, and its pack-
age manager is a tool responsible for storing and distributing thousands of third-party software
packages to the developer community. Yet, with greater interconnectivity comes greater vulner-
ability, a reality sharply highlighted in 2016 when removing the small utility left-pad package
from the npm registry. This event precipitated widespread software breakage as many web ap-
plications transitively and unknowingly depended on it for functionality.
This thesis uses complex network science to demonstrate how network measures can be used
to determine the structure and level of complexity of the npm network and, more interestingly,
how these parameters evolve over time. I analyse the npm network over five years, from 2012 to
2016. To the author’s knowledge, no study at the time of writing has analysed the npm package
ecosystem at a version level from the perspective of complex network science.
This thesis finds that the npm network exhibits small-world behaviour and a scale-free archi-
tecture, concurring with existing studies on open-source software systems. It underscores the
pivotal role of hierarchical software design in moulding npm’s network topology and identifies
versioned packages that disproportionately influence the network’s functionality. Notably, it re-
veals that central nodes can have up to 200,000 reverse transitive dependencies, highlighting
the ecosystem’s vulnerability to cascading failures. By providing a detailed exploration of npm’s
complex dependency network, this research deepens our understanding of npm’s infrastruc-
ture and highlights the critical network dynamics at play in open-source software development.
These insights pave the way for further research on mitigating potential vulnerabilities and im-
proving the resilience of software dependency networks.

-------

## 2-Small World with High Risks: A Study of Security Threats in the npm Ecosystem
Abstract
In response to the dynamic and ever-evolving landscape of network attacks and cybersecurity, this study aims to enhance network security by identifying critical nodes and optimizing resource allocation within budget constraints. We introduce a novel approach leveraging node centrality scores from four widely-recognized centrality measures. Our unique contribution lies in converting these centrality metrics into actionable insights for identifying network attack probabilities, providing an
unconventional yet effective method to bolster network robustness. Additionally, we propose a closed-form expression corre-
lating network robustness with node-centric features, including importance scores and attack probabilities. At the core of our
approach lies the development of a nonlinear optimization model that integrates predictive insights into node attack likelihood.
Through this framework, we successfully determine an optimal resource allocation strategy, minimizing cyberattack risks on
critical nodes while maximizing network robustness. Numerical results validate our approach, offering further insights into
network dynamics and improved resilience against emerging cybersecurity threats.


Keywords Centrality measure · Node detection · Performance evaluation · Optimization · Network security

-------

## 3-Node package manager’s dependency network robustness
The robustness of npm dependency network is a crucial property,
since many projects and web applications heavily rely on the func-
tionalities of packages, especially popular ones that have many de-
pendant packages. In the past, there have been instances where the
removal or update of certain npm packages has caused widespread
chaos and web-page downtime on the internet. Our goal is to track
the network’s resilience to such occurrences through time and fig-
ure out whether the state of the network is trending towards a more
robust structure. We show that the network is not robust to targeted
attacks, since a security risk in a few crucial nodes affects a large
part of the network. Because such packages are often backed up
by serious communities with high standards, the issue is not alarm-
ing and is a consequence of power law distribution of the network.
The current trend in average number of dependencies and effect of
important nodes on the rest of the network is decreasing, which fur-
ther improves the resilience and sets a positive path in development.
Furthermore, we show that communities form around the most im-
portant packages, although they do not conform well to the common
community definition using modularity. We also provide guidelines
for package development that increases the robustness of the net-
work and reduces the possibility of introducing security risks.

-------

## 4-On the Impact of Security Vulnerabilities in the npm Dependency Network
ABSTRACT
Security vulnerabilities are among the most pressing problems in
open source software package libraries. It may take a long time
to discover and fix vulnerabilities in packages. In addition, vul-
nerabilities may propagate to dependent packages, making them
vulnerable too. This paper presents an empirical study of nearly
400 security reports over a 6-year period in the npm dependency
network containing over 610k JavaScript packages. Taking into
account the severity of vulnerabilities, we analyse how and when
these vulnerabilities are discovered and fixed, and to which extent
they affect other packages in the packaging ecosystem in presence
of dependency constraints. We report our findings and provide
guidelines for package maintainers and tool developers to improve
the process of dealing with security issues.
KEYWORDS
software repository mining, software ecosystem, dependency net-
work, security vulnerability, semantic versioning

-------

## 5-Towards Using Package Centrality Trend to Identify Packages in Decline
Abstract—Due to their increasing complexity, today’s software
systems are frequently built by leveraging reusable code in the
form of libraries and packages. Software ecosystems (e.g., npm)
are the primary enablers of this code reuse, providing developers
with a platform to share their own and use others’ code. These
ecosystems evolve rapidly: developers add new packages every
day to solve new problems or provide alternative solutions,
causing obsolete packages to decline in their importance to the
community. Developers should avoid depending on packages in
decline, as these packages are reused less over time and may
become less frequently maintained. However, current popularity
metrics (e.g., Stars, and Downloads) are not fit to provide this
information to developers because their semantics do not aptly
capture shifts in the community interest.
In this paper, we propose a scalable approach that uses the
package’s centrality in the ecosystem to identify packages in
decline. We evaluate our approach with the npmecosystem
and show that the trends of centrality over time can correctly
distinguish packages in decline with an ROC-AUC of 0.9. The
approach can capture 87% of the packages in decline, on average
18 months before the trend is shown in currently used package
popularity metrics. We implement this approach in a tool that
can be used to augment the npms metrics and help developers
avoid packages in decline when reusing packages from npm.
Index Terms—JavaScript, Package Quality, Package in decline,
Dependency Graph, npm

-------
## 6-Demystifying vulnerability propagation via dependency trees in npm
ABSTRACT
Third-party libraries with rich functionalities facilitate the fast de-
velopment of JavaScript software, leading to the explosive growth
of the NPM ecosystem. However, it also brings new security threats
that vulnerabilities could be introduced through dependencies from
third-party libraries. In particular, the threats could be excessively
amplified by transitive dependencies. Existing research only con-
siders direct dependencies or reasoning transitive dependencies
based on reachability analysis, which neglects the NPM-specific
dependency resolution rules as adapted during real installation,
resulting in wrongly resolved dependencies. Consequently, further
fine-grained analysis, such as precise vulnerability propagation
and their evolution over time in dependencies, cannot be carried
out precisely at a large scale, as well as deriving ecosystem-wide
solutions for vulnerabilities in dependencies.
To fill this gap, we propose a knowledge graph-based depen-
dency resolution, which resolves the inner dependency relations
of dependencies as trees (i.e., dependency trees), and investigates
the security threats from vulnerabilities in dependency trees at a
large scale. Specifically, we first construct a complete dependency-
vulnerability knowledge graph (DVGraph) that captures the whole
NPM ecosystem (over 10 million library versions and 60 million
well-resolved dependency relations). Based on it, we propose a
novel algorithm (DTResolver) to statically and precisely resolve
dependency trees, as well as transitive vulnerability propagation
paths, for each package by taking the official dependency resolution
rules into account. Based on that, we carry out an ecosystem-wide
empirical study on vulnerability propagation and its evolution in
∗Also with Nanyang Technological University.†Sen Chen is the corresponding author.
Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation
on the first page. Copyrights for components of this work owned by others than ACM
must be honored. Abstracting with credit is permitted. To copy otherwise, or republish,
to post on servers or to redistribute to lists, requires prior specific permission and/or a
fee. Request permissions from permissions@acm.org.
ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA
©2022 Association for Computing Machinery.
ACM ISBN 978-1-4503-9221-1/22/05. . . $15.00
https://doi.org/10.1145/3510003.3510142
dependency trees. Our study unveils lots of useful findings, and
we further discuss the lessons learned and solutions for different
stakeholders to mitigate the vulnerability impact in NPM based on
our findings. For example, we implement a dependency tree based
vulnerability remediation method (DTReme) for NPM packages,
and receive much better performance than the official tool (npm
audit fix).
ACM Reference Format:
Chengwei Liu, Sen Chen, Lingling Fan, Bihuan Chen, Yang Liu, and Xin Peng.
2022. Demystifying the Vulnerability Propagation and Its Evolution via De-
pendency Trees in the NPM Ecosystem. In 44th International Conference on
Software Engineering (ICSE ’22), May 21–29, 2022, Pittsburgh, PA, USA. ACM,
New York, NY, USA, 

-------

## 7-On the Impact of Security Vulnerabilities in the npm and RubyGems Dependency Networks
Abstract The increasing interest in open source software has led to the emer-
gence of large language-specific package distributions of reusable software li-
braries, such as npm and RubyGems. These software packages can be sub-
ject to vulnerabilities that may expose dependent packages through explicitly
declared dependencies. Using Snyk’s vulnerability database, this article em-
pirically studies vulnerabilities affecting npm and RubyGems packages. We
analyse how and when these vulnerabilities are disclosed and fixed, and how
their prevalence changes over time. We also analyse how vulnerable packages
expose their direct and indirect dependents to vulnerabilities. We distinguish
between two types of dependents: packages distributed via the package man-
ager, and external GitHub projects depending on npm packages. We observe
that the number of vulnerabilities in npm is increasing and being disclosed
faster than vulnerabilities in RubyGems. For both package distributions, the
time required to disclose vulnerabilities is increasing over time. Vulnerabilities
in npm packages affect a median of 30 package releases, while this is 59 re-
leases in RubyGems packages. A large proportion of external GitHub projects
is exposed to vulnerabilities coming from direct or indirect dependencies. 33%
and 40% of dependency vulnerabilities to which projects and packages are ex-
posed, respectively, have their fixes in more recent releases within the same
major release range of the used dependency. Our findings reveal that more
effort is needed to better secure open source package distributions.
Keywords: security vulnerabilities, npm, RubyGems, vulnerable packages

-------

## 8- Towards Sustainable and Secure Reuse in Dependency Supply Chains
BRITTANY REID, Nara Institute of Science and Technology, Japan
RAULA GAIKOVINA KULA, The University of Osaka, Japan
Much of the success of modern software development can be attributed to code reuse. The ability to reuse existing functionality via
third-party dependencies has enabled massive gains in productivity, but for a long time the dominant philosophy has been to ‘reuse as
much as possible, without thought for what is being depended upon’, creating fragile dependency chains. Heavy reliance has raised
resiliency and maintenance concerns. In this vision paper, we investigate packages that challenge the typical concepts of reuse–that
is, packages with no dependencies themselves that bear the responsibility of being at the end of the dependency supply chain. By
avoiding dependencies, these packages at the end of the chain may also avoid the associated risks. Our initial analysis of the most
depended upon NPM packages shows that such end-of-chain packages make up a significant portion of these critical dependency chain
(over 50%). We find that these end-of-chain packages vary in characteristics and are not just packages that can be easily replaced, and
present five cases. We then ask ourselves: Should maintainers minimize external dependencies? We argue that these packages reveal
important lessons for strategic reuse—balancing the undeniable benefits of dependency ecosystems with sustainable, secure practices.
CCS Concepts: •Software and its engineering →Software libraries and repositories.
Additional Key Words and Phrases: Software Engineering, Software Ecosystems, Security and Maintenance
ACM Reference Format:
Brittany Reid and Raula Gaikovina Kula. 2025. Towards Sustainable and Secure Reuse in Dependency Supply Chains: Initial Analysis
of NPM packages at the End of the Chain . 1, 1 (October 2025), 12 pages

-------

## 9- Structural and Connectivity Patterns in the Maven Central Software Dependency Network
Abstract. Understanding the structural characteristics and connectivity patterns of large-scale soft-
ware ecosystems is critical for enhancing software reuse, improving ecosystem resilience, and mitigating
security risks. In this paper, we investigate the Maven Central ecosystem, one of the largest repositories
of Java libraries, by applying network science techniques to its dependency graph. Leveraging the Goblin
framework, we extracted a sample consisting of the top 5,000 highly connected artifacts based on their
degree centrality and then performed breadth-first search (BFS) expansion from each selected artifact
as a seed node, traversing the graph outward to capture all libraries and releases reachable those seed
nodes. This sampling strategy captured the immediate structural context surrounding these libraries
resulted in a curated graph comprising of 1.3 million nodes and 20.9 million edges. We conducted a
comprehensive analysis of this graph, computing degree distributions, betweenness centrality, PageRank
centrality, and connected components graph-theoretic metrics. Our results reveal that Maven Central
exhibits a highly interconnected, scale-free, and small-world topology, characterized by a small number
of infrastructural hubs that support the majority of projects. Further analysis using PageRank and
betweenness centrality shows that these hubs predominantly consist of core ecosystem infrastructure,
including testing frameworks and general-purpose utility libraries. While these hubs facilitate efficient
software reuse and integration, they also pose systemic risks; failures or vulnerabilities affecting these
critical nodes can have widespread and cascading impacts throughout the ecosystem.
Keywords: Software dependencies, Dependencies network analysis, Maven central repository, Software
security, Software ecosystems, Network data mining

-------

## 10- VulRG: Multi-Level Explainable Vulnerability Patch Ranking for Complex Systems Using Graphs
As interconnected systems proliferate, safeguarding complex infrastructures against an escalating array of
cyber threats has become an urgent challenge. The growing number of vulnerabilities, coupled with resource
constraints, makes addressing every vulnerability impractical, thereby rendering effective prioritization
essential. However, current risk prioritization methods, which often rely on expert judgment or focus solely
on exploit likelihood and consequences, lack the granularity and adaptability needed for complex systems.
This paper presents a novel graph-based framework for patch prioritization that optimizes security in complex
systems by integrating diverse data sources and metrics into a universally applicable model. We introduce
refined risk metrics that enable detailed assessments at the component, asset, and system levels. The framework
employs two key graphs: a network communication graph to model potential attack paths and identify the
shortest routes to critical assets, and a system dependency graph to capture risk propagation from exploited
vulnerabilities across interconnected components. By defining asset criticality and component dependency
rules, our approach systematically assesses and mitigates risks. Benchmarking against state-of-the-art methods
demonstrates our framework’s superior accuracy in vulnerability patch ranking, with enhanced explainability.
This framework not only advances vulnerability management but also sets the stage for future research in
adaptive cybersecurity strategies.
CCS Concepts: •Security and privacy →Systems security; Vulnerability management.
Additional Key Words and Phrases: Risk Metrics, Risk Aggregation, Vulnerability Prioritization, Patch Rank,
Cybersecurity
ACM Reference Format:
Yuning Jiang, Nay Oo, Qiaoran Meng, Hoon Wei Lim, and Biplab Sikdar. 2025. VulRG: Multi-Level Explainable
Vulnerability Patch Ranking for Complex Systems Using Graphs. 1, 1 (February 2025), 32 pages

-------

## 11- Predicting nodal influence via local iterative metrics
Nodal spreading influence is the capability of a node to activate the rest of the network when it is 
the seed of spreading. Combining nodal properties (centrality metrics) derived from local and global 
topological information respectively has been shown to better predict nodal influence than using a 
single metric. In this work, we investigate to what extent local and global topological information 
around a node contributes to the prediction of nodal influence and whether relatively local 
information is sufficient for the prediction. We show that by leveraging the iterative process used to 
derive a classical nodal centrality such as eigenvector centrality, we can define an iterative metric set 
that progressively incorporates more global information around the node. We propose to predict nodal 
influence using an iterative metric set that consists of an iterative metric from order 1 to K produced 
in an iterative process, encoding gradually more global information as K increases. Three iterative 
metrics are considered, which converge to three classical node centrality metrics, respectively. In 
various real-world networks and synthetic networks with community structures, we find that the 
prediction quality of each iterative based model converges to its optimal when the metric of relatively 
low orders ( K∼4 ) are included and increases only marginally when further increasing K. This fast 
convergence of prediction quality with K is further explained by analyzing the correlation between 
the iterative metric and nodal influence, the convergence rate of each iterative process and network 
properties. The prediction quality of the best performing iterative metric set with K=4 is comparable 
with the benchmark method that combines seven centrality metrics: their prediction quality ratio 
is within the range [91%,106%] across all three quality measures and networks. In two spatially 
embedded networks with an extremely large diameter, however, iterative metric of higher orders, 
thus a large K, is needed to achieve comparable prediction quality with the benchmark.


-------

## 12- Securing Network Resilience: Leveraging Node Centrality for Cyberattack Mitigation and Robustness Enhancement

Essia Hamouda1 ·Mohsen ElHafsi2 ·Joon Son1
Accepted: 19 February 2024
© The Author(s), under exclusive licence to Springer Science+Business Media, LLC, part of Springer Nature 2024
Abstract
In response to the dynamic and ever-evolving landscape of network attacks and cybersecurity, this study aims to enhance
network security by identifying critical nodes and optimizing resource allocation within budget constraints. We introduce a
novel approach leveraging node centrality scores from four widely-recognized centrality measures. Our unique contribution
lies in converting these centrality metrics into actionable insights for identifying network attack probabilities, providing an
unconventional yet effective method to bolster network robustness. Additionally, we propose a closed-form expression corre-
lating network robustness with node-centric features, including importance scores and attack probabilities. At the core of our
approach lies the development of a nonlinear optimization model that integrates predictive insights into node attack likelihood.
Through this framework, we successfully determine an optimal resource allocation strategy, minimizing cyberattack risks on
critical nodes while maximizing network robustness. Numerical results validate our approach, offering further insights into
network dynamics and improved resilience against emerging cybersecurity threats.
Keywords Centrality measure · Node detection · Performance evaluation · Optimization · Network security


-------


