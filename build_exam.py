#!/usr/bin/env python3
"""Generate a hard, open-book-style 100-question MCQ practice exam (PDF)
from 'Business: Markets & Organizations' notes, with a separate answer key
and explanations referencing the relevant chapter/section.
"""
import html
import re
import fitz  # PyMuPDF

OUT = "Business - Practice Exam (100 MCQs).pdf"
HTML_OUT = "Business - Practice Exam (100 MCQs).html"

# ---------------------------------------------------------------------------
# QUESTION BANK
# Each item: (topic, question, [options], [correct_indices], explanation)
# A trailing "*" was NOT used; correctness is given by the index list.
# multi-select questions state "(Select TWO/THREE)" in the stem.
# ---------------------------------------------------------------------------
Q = []
def add(topic, q, opts, ans, exp):
    Q.append(dict(topic=topic, q=q, opts=opts, ans=ans, exp=exp))

# ===== Ch1 — Markets vs Organizations =====
T = "Chapter 1 — Markets vs Organizations"
add(T, "The 'economic problem', as defined in the notes, refers specifically to:",
    ["The tendency of competitive markets to drive profits to zero in the long run",
     "A situation in which needs cannot be met because of the scarcity of natural, human and man-made resources",
     "The inability of managers to act in the interest of shareholders",
     "The systematic errors people make when judging under uncertainty"],
    [1], "Ch1 \u00a71.1: the economic problem stems from scarcity; efficiency means resources are allocated optimally.")
add(T, "'Progressive division of labour' is linked to which outcome, and what is its main organizational limit?",
    ["Higher productivity, limited only by consumer demand",
     "Higher productivity, but insufficient collaboration on new challenges, requiring more coordination",
     "Lower transaction costs, limited by asset specificity",
     "Higher utility, limited by bounded rationality"],
    [1], "Ch1 \u00a71.2\u20131.3: division of labour raises productivity; the limit is reduced collaboration, which demands more coordination.")
add(T, "Which pairing of coordinating mechanism to institution is correct?",
    ["Market \u2192 authority (non-price); Organization \u2192 price system",
     "Market \u2192 price system (no personal interaction); Organization \u2192 authority (non-price)",
     "Both rely primarily on the price system",
     "Market \u2192 standardization of norms; Organization \u2192 mutual adjustment"],
    [1], "Ch1 \u00a71.5: the market coordinates via the price system; organizations via authority. Choose the less costly; organizations handle information problems better.")
add(T, "(Select TWO) Which of the following are *informal* institutions?",
    ["Written constitutions", "Norms of behaviour", "Government regulations",
     "Conventions / internally imposed rules of conduct", "Statutory laws"],
    [1, 3], "Ch1 \u00a71.7: formal = written laws/constitutions/regulations; informal = norms of behaviour and conventions.")
add(T, "The *environment* of markets and organizations performs all of the following roles EXCEPT:",
    ["Providing the conditions for organizations/markets to be created",
     "Shaping organizations/markets by exerting pressure",
     "Acting as a selection mechanism determining which can succeed",
     "Eliminating bounded rationality among economic actors"],
    [3], "Ch1 \u00a71.7: the environment provides conditions, exerts pressure and selects; it does not remove bounded rationality.")

# ===== Ch2 — Markets =====
T = "Chapter 2 — Markets"
add(T, "At market equilibrium:",
    ["Quantity demanded exceeds quantity supplied, pushing prices up",
     "The quantity demanded equals the quantity supplied at the market price",
     "Producers maximize utility and consumers maximize profit",
     "There are, by definition, no transaction costs"],
    [1], "Ch2 \u00a72.2: equilibrium is where quantity demanded = quantity supplied at the market price.")
add(T, "A profit-maximizing firm's production function makes profit depend on:",
    ["Only the market price",
     "The quantity produced (Q), the capital (K) and the labour (L) used",
     "The utility derived by consumers",
     "The degree of asset specificity"],
    [1], "Ch2 \u00a72.4: profit depends on Q, K and L; the firm chooses the optimal K/L mix to maximize profit.")
add(T, "The 'paradox of profits' states that:",
    ["Monopolists always earn supernormal profits",
     "In a competitive market, although each firm tries to maximize profit, no firm can profit in the long run",
     "Profits rise with the number of competitors",
     "Profit maximization is impossible under bounded rationality"],
    [1], "Ch2 \u00a72.6: in a competitive market profit-seeking by all firms competes profits away in the long run.")
add(T, "(Select TWO) Which conditions are required for a *perfect market*?",
    ["A few large buyers/sellers who set the price", "Homogeneous product",
     "Zero transaction costs", "High entry barriers protecting incumbents",
     "Asymmetric information favouring sellers"],
    [1, 2], "Ch2 \u00a72.7: many small buyers/sellers, free entry/exit, homogeneous product, perfect information, zero transaction costs.")
add(T, "When consumer demand increases, the adjustment toward a new equilibrium is:",
    ["Producers cut output to raise prices",
     "Consumers buy more \u2192 producers produce more \u2192 a new market equilibrium",
     "The price mechanism fails and authority is needed",
     "The product becomes non-rival"],
    [1], "Ch2 \u00a72.2: higher demand leads consumers to buy more and producers to supply more until a new equilibrium is reached.")

# ===== Ch3 — Organisations =====
T = "Chapter 3 — Organisations"
add(T, "Which Mintzberg component 'joins the strategic apex to the operating core'?",
    ["Technostructure", "Support staff", "Middle line", "Ideology"],
    [2], "Ch3 \u00a73.1: the middle line (branch managers) links the strategic apex to the operating core.")
add(T, "The technostructure (analysts, accountants, engineers) primarily:",
    ["Provides the basic operating work",
     "Uses analytical techniques to achieve standardization and efficiency",
     "Carries out direct supervision and strategy",
     "Indirectly supports the operating core (e.g. legal, PR)"],
    [1], "Ch3 \u00a73.1: the technostructure standardizes for efficiency; indirect support (legal/PR) is the support staff.")
add(T, "A hospital that coordinates mainly through *standardization of skills*, giving trained specialists in the operating core high discretion, is which type?",
    ["Machine", "Professional", "Diversified", "Missionary"],
    [1], "Ch3 \u00a73.3: the professional organization relies on standardization of skills.")
add(T, "Match the organization type to its primary coordinating mechanism. Which pairing is INCORRECT?",
    ["Machine \u2192 standardization of work processes",
     "Diversified \u2192 standardization of outputs",
     "Innovative \u2192 direct supervision",
     "Missionary \u2192 standardization of norms / ideology"],
    [2], "Ch3 \u00a73.3: the innovative organization coordinates by mutual adjustment, not direct supervision.")
add(T, "In the *diversified* organization:",
    ["Divisions have full decision-making autonomy, HQ manages all divisions, and coordination is by standardization of outputs",
     "The entrepreneur coordinates by direct supervision",
     "Coordination is achieved by standardization of skills",
     "Decision-making is distributed among staff experts via mutual adjustment"],
    [0], "Ch3 \u00a73.3: diversified = autonomous divisions serving different markets, coordinated by standardized outputs.")
add(T, "(Select TWO) Which are examples of *internal markets* inside an organization?",
    ["Internal capital market (corporate mgmt funds the highest-return divisions)",
     "The external market for corporate control",
     "Internal labour market (divisions compete for the best people)",
     "An open ascending auction with external bidders"],
    [0, 2], "Ch3 \u00a73.4: internal markets for goods, capital and labour operate within the organization.")
add(T, "Which feature is NOT listed as a driver of a *platform organization's* success?",
    ["Scalability through low-cost replication",
     "Direct/indirect network effects with positive feedback loops",
     "First-mover advantage",
     "Standardization of skills among the operating core"],
    [3], "Ch3 \u00a73.8: scalability, network effects, first-mover advantage and high valuation drive platforms.")

# ===== Ch4 — Information =====
T = "Chapter 4 — Information"
add(T, "Adverse selection is best characterized as:",
    ["An ex post (hidden action) problem",
     "An ex ante (hidden information) problem that can preclude a transaction",
     "A coordination failure between two equal players",
     "A non-rival good problem"],
    [1], "Ch4 \u00a74.2: adverse selection = hidden information, an ex ante problem.")
add(T, "Moral hazard is:",
    ["An ex ante problem solved by signaling",
     "An ex post (hidden action) problem where a protected party takes a risk whose cost falls on the other",
     "Identical to the winner's curse",
     "A property of perfect markets"],
    [1], "Ch4 \u00a74.3: moral hazard = hidden action, an ex post problem.")
add(T, "Distinguish signaling from screening:",
    ["Signaling: the uninformed party induces disclosure; Screening: the informed party discloses",
     "Signaling: the informed (1st) party reveals private info; Screening: the 2nd party tempts the 1st to reveal it",
     "Both refer to vertical integration",
     "Both are market failures with no solution"],
    [1], "Ch4 \u00a74.2: signaling = informed party reveals; screening = uninformed party induces revelation.")
add(T, "A supermarket uncertain about future fruit quality signs a contract specifying prices contingent on actual delivered quality. This is:",
    ["A contingent claims contract \u2014 a *market* solution to information uncertainty",
     "Vertical integration \u2014 an organizational solution",
     "A joint venture \u2014 an organizational solution to asymmetry",
     "Screening"],
    [0], "Ch4 \u00a74.1: for uncertainty, the market solution is a contingent claims contract; the organizational solution would be vertical integration.")
add(T, "(Select TWO) Information is an *economic good* because it is:",
    ["Rival in consumption", "Non-rival (usable by many at once)",
     "Costly to reproduce", "Low in reproduction cost"],
    [1, 3], "Ch4 \u00a74.5: information is non-rival with low reproduction cost.")
add(T, "The classic used-car ('lemons') situation, where the seller knows quality and the buyer does not before the deal, is an instance of:",
    ["Moral hazard", "Adverse selection (hidden information, ex ante)",
     "The endowment effect", "The free-rider problem"],
    [1], "Ch4 \u00a74.2: pre-contract private information about quality is adverse selection.")

# ===== Ch5 — Game theory =====
T = "Chapter 5 — Game theory"
add(T, "A Nash equilibrium is defined as:",
    ["The combination of each player's dominant strategy",
     "A state where each player makes an optimal choice given the other player's choice",
     "The outcome that maximizes total welfare",
     "Any outcome of a sequential game"],
    [1], "Ch5 \u00a75.2: Nash equilibrium = each player optimizes given the other's choice (dominant-strategy equilibrium is a special case).")
add(T, "In a *sequential* coordination game, the notes state that:",
    ["Both players must move simultaneously",
     "The first player to move has an advantage",
     "There is never a Nash equilibrium",
     "The winner's curse always arises"],
    [1], "Ch5 \u00a75.3: in sequential games the first mover has an advantage.")
add(T, "The principle of 'looking ahead and reasoning backwards through the game tree' applies to:",
    ["Single-stage auctions", "The prisoner's dilemma only",
     "Sequential / entry games where you anticipate the rival's response",
     "The endowment effect"],
    [2], "Ch5 \u00a75.4: entry/sequential games require anticipating the rival and reasoning backwards.")
add(T, "For a threat to deter entry it must be:",
    ["Secret and reversible", "Observable and credible (showing commitment)",
     "Profitable only in the short run", "Backed by collusion"],
    [1], "Ch5 \u00a75.4: credible threats must be observable and demonstrate commitment.")
add(T, "(Select TWO) Which statements about auctions are correct?",
    ["In an open auction, bids are observable and private info is revealed during competition",
     "In a sealed-bid auction the winner's curse is a potential problem for the buyer",
     "Sealed-bid auctions reveal all private information",
     "An open auction guarantees the seller the highest possible price"],
    [0, 1], "Ch5 \u00a75.6: open auctions reveal info; sealed-bid auctions risk the winner's curse (buyer) and collusion.")
add(T, "The guidance on the *best coordination solution* by number of players is:",
    ["Two players \u2192 standardization; many players \u2192 mutual adjustment",
     "Two players \u2192 mutual adjustment; many players \u2192 standardization / direct supervision",
     "Always use direct supervision",
     "Always use the price mechanism"],
    [1], "Ch5 \u00a75.3: two players coordinate by mutual adjustment; many players need standardization/direct supervision.")

# ===== Ch6 — Econs / humans (behavioural economics) =====
T = "Chapter 6 — Econs / Humans"
add(T, "The 'econ' vs 'human' distinction is:",
    ["Econ = boundedly rational; human = fully rational",
     "Econ (microeconomics) = rational/selfish; human (behavioural) = not always rational/selfish",
     "Both are always rational",
     "'Human' refers only to managers"],
    [1], "Ch6 \u00a76.1: microeconomics assumes a rational/selfish 'econ'; behavioural economics studies the 'human'.")
add(T, "Relying too heavily on an early piece of information when deciding is:",
    ["Availability", "Anchoring", "Representativeness", "Framing"],
    [1], "Ch6 \u00a76.4: anchoring = over-reliance on an early piece of information.")
add(T, "Valuing a good you already own more than your willingness to pay for it before owning it is:",
    ["Mental accounting", "The endowment effect", "Framing", "The free-rider problem"],
    [1], "Ch6 \u00a76.4: the endowment effect over-values goods already held.")
add(T, "(Select TWO) Prospect theory holds that:",
    ["People evaluate gambles in terms of final wealth levels",
     "People evaluate gambles in terms of *changes* in wealth",
     "People hate losing more than they love gaining (loss aversion)",
     "Sensitivity falls to zero for large gains/losses"],
    [1, 2], "Ch6 \u00a76.5: people evaluate changes in wealth and are loss-averse; sensitivity rises with the size of gain/loss.")
add(T, "Basing a prediction on the class of cases an individual seems to belong to, jumping to conclusions, is:",
    ["Representativeness", "Anchoring", "Mental accounting", "Endowment effect"],
    [0], "Ch6 \u00a76.4: representativeness judges by the class rather than the individual case.")
add(T, "The social-vs-economic-domain point is that:",
    ["Offering payment is always beneficial",
     "Payment fits the economic domain but may not fit the social domain; moving issues across domains is not necessarily beneficial",
     "Social and economic domains are identical",
     "Nudging only works in the economic domain"],
    [1], "Ch6 \u00a76.2: what is correct in the economic domain (payment) can be inappropriate in the social domain.")

# ===== Ch7 — Behavioural theory of the firm =====
T = "Chapter 7 — Behavioural Theory"
add(T, "Behavioural theory views the firm as:",
    ["A holistic profit-maximizing entity",
     "A coalition of participants (stakeholders), each boundedly rational with individual goals",
     "A nexus of contracts with irrelevant ownership",
     "A peer group with no hierarchy"],
    [1], "Ch7 \u00a77.1\u20137.2: the firm is a coalition of participants with their own goals.")
add(T, "A participant continues to contribute to the organization as long as:",
    ["Contribution \u2265 inducement", "Inducement \u2265 contribution",
     "Profit is maximized", "The aspiration level is zero"],
    [1], "Ch7 \u00a77.2: participants contribute while inducements \u2265 contributions.")
add(T, "Organizational goals emerge from bargaining; a member's bargaining power depends on:",
    ["Seniority alone", "How unique the contribution offered to the coalition is",
     "The number of shares held", "The level of asset specificity"],
    [1], "Ch7 \u00a77.3: bargaining power rises with the uniqueness of one's contribution.")
add(T, "Organizational choice is described as:",
    ["Optimizing over all alternatives simultaneously (full rationality)",
     "Evaluating alternatives one at a time, seeking a solution that satisfies aspiration levels and is acceptable to stakeholders (satisficing)",
     "Always selecting the profit-maximizing option",
     "Random selection under uncertainty"],
    [1], "Ch7 \u00a77.5: firms satisfice \u2014 they search until an acceptable, aspiration-satisfying option is found.")
add(T, "'Requiring teams to go through checklists to reduce errors' is which method of improving rationality?",
    ["Nudging", "Encouraging dissent", "Routines", "Debiasing training"],
    [2], "Ch7 \u00a77.6: routines (e.g. checklists) reduce errors and improve effectiveness.")
add(T, "Per \u00a77.4, two people in the same firm with the *same* information may still:",
    ["Always reach the same decision",
     "Hold different expectations that influence their decision-making",
     "Be perfectly rational", "Eliminate all bias"],
    [1], "Ch7 \u00a77.4: identical information can still yield different expectations and decisions.")

# ===== Ch8 — Agency theory =====
T = "Chapter 8 — Agency Theory"
add(T, "Agency theory concerns:",
    ["The relationship between two competing firms",
     "The relationship between a principal and an agent who takes decisions for the principal",
     "Coordination between equal peers",
     "Auctions with many bidders"],
    [1], "Ch8 \u00a78.1: agency theory studies principal\u2013agent relations (owner\u2013manager, etc.).")
add(T, "(Select THREE) Which *markets* discipline managers against on-the-job consumption?",
    ["Stock market", "Market for corporate control", "Market for managerial labour",
     "The endowment market", "The data room"],
    [0, 1, 2], "Ch8 \u00a78.2: the stock market, the market for corporate control, the managerial-labour market and the product market discipline managers.")
add(T, "When a manager-owner sells part of her shares to an outside investor, the notes predict she will:",
    ["Consume less on the job", "Engage in *more* on-the-job consumption",
     "Always increase firm value", "Eliminate the agency problem"],
    [1], "Ch8 \u00a78.3: selling shares increases on-the-job consumption; monitoring then reduces it, and the manager captures the value gain.")
add(T, "Under asymmetric information with a *risk-averse* agent, the optimal contract is:",
    ["A forcing contract", "A wage contract (fixed salary independent of pay-off; principal bears risk)",
     "A rent contract (agent gets pay-off minus a fixed amount)", "No contract is possible"],
    [1], "Ch8 \u00a78.6: risk-averse agent + risk-bearing principal \u2192 fixed wage contract.")
add(T, "A *rent contract* (agent receives the pay-off minus a fixed amount) is appropriate when the agent is:",
    ["Risk-averse", "Risk-neutral", "Boundedly rational only", "The principal"],
    [1], "Ch8 \u00a78.6: a risk-neutral agent can bear risk via a rent contract.")
add(T, "In the 'solution to moral hazard in teams' view, the manager is essential because:",
    ["Ownership is irrelevant",
     "Team production can create free-riding (shirking); the manager supervises to produce extra output",
     "The firm is just a nexus of contracts",
     "Markets always outperform firms"],
    [1], "Ch8 \u00a78.4 / theories-of-the-firm: the supervising manager curbs team shirking and enables extra output.")
add(T, "In a large public corporation, the notes distinguish:",
    ["Decision management (diffused among managers) from decision control (exercised by the board for shareholders)",
     "Decision management exercised solely by shareholders",
     "No separation of functions",
     "Control held by the operating core"],
    [0], "Ch8 \u00a78.5: decision management is diffused; decision control rests with the board on behalf of shareholders.")

# ===== Ch9 — Transaction Cost Economics =====
T = "Chapter 9 — Transaction Cost Economics"
add(T, "TCE says the choice between market and organization is fundamentally:",
    ["A matter of maximizing utility",
     "A matter of cost minimization (transaction costs + production costs)",
     "Determined only by asset specificity",
     "Independent of bounded rationality"],
    [1], "Ch9 \u00a79.1: allocate a transaction to market or firm to minimize transaction + production costs.")
add(T, "(Select TWO) The two behavioural assumptions underlying TCE are:",
    ["Bounded rationality", "Perfect information", "Opportunism", "Risk neutrality"],
    [0, 2], "Ch9 \u00a79.1\u20139.2: humans are boundedly rational and sometimes opportunistic.")
add(T, "The 'fundamental transformation' refers to:",
    ["A move from organization to market coordination",
     "A large-numbers exchange turning into a small-numbers exchange because one supplier gains superiority",
     "Digitization lowering transaction costs",
     "Conversion of a peer group into a hierarchy"],
    [1], "Ch9 \u00a79.2: ex post, large-numbers competition can collapse into small-numbers bargaining.")
add(T, "Asset specificity means an asset:",
    ["Can be redeployed to other uses at no loss",
     "Cannot be redeployed to an alternative use without a significant loss of value (high specificity \u2192 high market transaction cost)",
     "Is always intangible",
     "Is owned jointly by a peer group"],
    [1], "Ch9 \u00a79.3: specific assets lose value if redeployed; high specificity raises market transaction costs.")
add(T, "The three critical dimensions of transactions are:",
    ["Price, quantity, quality",
     "Asset specificity, uncertainty/complexity, frequency",
     "Signaling, screening, monitoring",
     "Bounded rationality, opportunism, atmosphere"],
    [1], "Ch9 \u00a79.3: transaction costs depend on asset specificity, uncertainty/complexity and frequency.")
add(T, "(Select TWO) Advantages of a *peer group* over working independently include:",
    ["Economies of scale (joint ownership, shared information)",
     "Elimination of all shirking regardless of size",
     "Risk-bearing and associational gains",
     "A boss with the right to adjust pay"],
    [0, 2], "Ch9 \u00a79.4: peer groups gain scale, risk-bearing and associational advantages; shirking becomes a problem only in large groups.")
add(T, "The key advantage of a *simple hierarchy* over a peer group is that:",
    ["It eliminates the price mechanism",
     "A boss monitors employees (reducing shirking) and decision-making/communication is more economical",
     "Risk is shared more widely", "It removes asset specificity"],
    [1], "Ch9 \u00a79.5: a boss monitors to reduce shirking and economizes on communication/decisions.")
add(T, "Compared with the U-form, the M-form enterprise:",
    ["Suffers more cumulative control loss because information crosses many layers",
     "Splits the firm into quasi-autonomous (usually product) divisions, with corporate staff advising + auditing and top managers focused on strategy",
     "Has no corporate staff", "Coordinates purely by mutual adjustment"],
    [1], "Ch9 \u00a79.6: cumulative control loss is the U-form weakness; the M-form uses quasi-autonomous divisions + corporate staff.")
add(T, "Trust in TCE is described such that:",
    ["Personal trust matters in impersonal exchanges",
     "Personal trust reduces opportunism inside firms; impersonal trust (institutions/reputation) matters in impersonal exchanges",
     "Trust is irrelevant once contracts exist",
     "Only impersonal trust reduces shirking"],
    [1], "Ch9 \u00a79.9: personal trust works inside firms/personal exchanges; impersonal trust governs impersonal exchanges.")

# ===== Ch10 — Competitive strategy =====
T = "Chapter 10 — Competitive Strategy"
add(T, "Corporate vs competitive strategy:",
    ["Corporate = how to compete in one industry; Competitive = where to compete",
     "Corporate = where a multi-business firm competes (portfolio); Competitive = how a single business unit competes",
     "They are synonyms", "Both are purely descriptive"],
    [1], "Ch10 \u00a710.1: corporate strategy = where (portfolio); competitive strategy = how a business unit competes.")
add(T, "The S-C-P paradigm holds that:",
    ["Conduct determines structure, which determines performance",
     "Industry structure \u2192 firm conduct \u2192 industry performance",
     "Performance determines structure", "Strategy is irrelevant to performance"],
    [1], "Ch10 \u00a710.2: structure shapes conduct, which determines performance.")
add(T, "Under Porter's five forces, the collective strength of the forces determines profit potential such that:",
    ["Stronger forces \u2192 weaker competition \u2192 higher profits",
     "Weaker forces \u2192 weaker competition \u2192 higher profit potential",
     "Forces have no effect on profitability", "Only rivalry matters"],
    [1], "Ch10 \u00a710.2: the weaker the forces, the weaker the competition and the higher the profit potential.")
add(T, "(Select TWO) A *supplier* group is powerful when:",
    ["It is dominated by a few companies",
     "Its product is standard and undifferentiated",
     "It poses a credible threat of forward integration",
     "The industry is its single most important customer"],
    [0, 2], "Ch10 \u00a710.2: powerful suppliers are concentrated, sell differentiated products and can threaten forward integration.")
add(T, "A *buyer* group is powerful when, among others:",
    ["It purchases in small volumes",
     "The products it buys are differentiated and unique",
     "It buys standard/undifferentiated products that form a significant fraction of its cost",
     "The product is critical to the quality of the buyer's own product"],
    [2], "Ch10 \u00a710.2: buyers are strong when buying large volumes of standard goods that are a big share of their costs.")
add(T, "Cost leadership vs differentiation:",
    ["Cost leadership relies on brand recognition and high advertising",
     "Cost leadership = lowest unit cost (via scale/experience, aided by large market share); differentiation = a product perceived as more valuable, allowing a higher price",
     "Differentiation requires the lowest possible unit cost", "They are the same strategy"],
    [1], "Ch10 \u00a710.4: cost leadership minimizes unit cost; differentiation commands a price premium for perceived value.")
add(T, "The VRIN criteria require resources to be:",
    ["Valuable, rare, inimitable, non-substitutable \u2014 and intangible resources are more likely to satisfy them",
     "Visible, replicable, internal, networked",
     "Valuable but easily imitated", "Tangible to be sustainable"],
    [0], "Ch10 \u00a710.5: VRIN resources confer sustainable advantage; intangibles tend to meet VRIN more than tangibles.")
add(T, "'Isolating mechanisms' in the dynamic-capabilities discussion:",
    ["Prevent other firms from competing away the profit a firm earns from its capability",
     "Are the same as economies of scale",
     "Refer to first-mover pricing", "Eliminate tacit knowledge"],
    [0], "Ch10 \u00a710.6: isolating mechanisms protect a capability's profits from imitation.")

# ===== Ch11 — Corporate strategy =====
T = "Chapter 11 — Corporate Strategy"
add(T, "'A supplies components to B (or vice versa)' describes which corporate-strategy type?",
    ["Vertical integration", "Horizontal multi-nationalization",
     "Related diversification", "Conglomerate diversification"],
    [0], "Ch11 \u00a711.1: a supplier\u2013customer link between A and B is vertical integration.")
add(T, "'A and B operate in the same industry but in different countries' describes:",
    ["Vertical integration", "Horizontal multi-nationalization",
     "Related diversification", "Conglomerate diversification"],
    [1], "Ch11 \u00a711.1: same industry, different countries = horizontal multi-nationalization.")
add(T, "In a *conglomerate*, for debt financing, diversification across unrelated industries:",
    ["Increases the chance of bankruptcy", "Reduces the chance of bankruptcy",
     "Has no effect on transaction costs", "Requires economies of scope"],
    [1], "Ch11 \u00a711.2: spreading across industries lowers bankruptcy risk, reducing financing transaction costs.")
add(T, "Why might corporate HQ allocate capital better than outside investors?",
    ["It has less information than the market",
     "Business-unit managers share confidential information with HQ that they would not reveal to external investors, and HQ may have specialized knowledge",
     "It avoids the principal-agent problem entirely", "It eliminates asset specificity"],
    [1], "Ch11 \u00a711.2: HQ's information advantage and specialized knowledge improve internal capital allocation.")
add(T, "Related diversification is especially motivated by *economies of scope*, which exist when:",
    ["Producing two goods jointly is *less* costly than producing them separately",
     "A single product is mass-produced at scale",
     "Two unrelated businesses are combined", "The price mechanism fails entirely"],
    [0], "Ch11 \u00a711.3: economies of scope = cheaper joint production of two goods than separate production.")
add(T, "When economies of scope depend on *intangible* assets (know-how, brand), the notes argue:",
    ["Market transactions are clearly preferred",
     "HQ (the corporate form) is preferred because it facilitates cooperation between businesses",
     "A peer group is optimal", "Vertical integration is never viable"],
    [1], "Ch11 \u00a711.3: intangibles are costly to trade, so the corporate form (HQ) is preferred.")
add(T, "In the vertical-integration decision matrix, which case most clearly calls for *vertical integration*?",
    ["Asset specificity low on both sides, low uncertainty (\u2192 spot contracts)",
     "Mutually high asset specificity, low uncertainty (\u2192 long-term contract)",
     "High asset specificity on both sides with high uncertainty/complexity",
     "Low asset specificity, high uncertainty, low frequency"],
    [2], "Ch11 \u00a711.5: high mutual asset specificity + high uncertainty \u2192 vertical integration.")

# ===== Ch14 — Mergers & Acquisitions =====
T = "Chapter 14 — Mergers & Acquisitions"
add(T, "A *merger* (vs an acquisition) is defined as:",
    ["One firm taking a controlling interest in another while both survive",
     "A combination of firms in which all but one cease to exist and the combined entity continues under the surviving firm's name",
     "Any purchase of selected assets", "A joint venture"],
    [1], "Ch14 \u00a714.1: a merger absorbs all but one firm; an acquisition is taking a controlling interest.")
add(T, "Backward vs forward vertical integration through M&A:",
    ["Backward = buying a former customer; Forward = buying a former supplier",
     "Backward = buying a former supplier; Forward = buying a former customer",
     "Both mean buying a competitor", "Both are conglomerate mergers"],
    [1], "Ch14 \u00a714.1: backward = buy a supplier; forward = buy a customer.")
add(T, "*Event studies* (corporate finance) differ from *outcome studies* (industrial organization) in that:",
    ["Event studies compare pre/post profits; outcome studies look at announcement share prices",
     "Event studies examine abnormal share-price returns at announcement; outcome studies compare pre- and post-M&A performance",
     "They are identical", "Neither studies performance"],
    [1], "Ch14 \u00a714.3: event studies = abnormal returns at announcement; outcome studies = pre/post performance.")
add(T, "(Select TWO) The empirical M&A findings reported are:",
    ["Shareholders of the acquired (target) firm gain",
     "Shareholders of the acquiring firm earn large permanent gains",
     "Acquiring-firm shareholders see an initial loss then break even",
     "The net change in combined market value is negative"],
    [0, 2], "Ch14 \u00a714.3: targets gain, acquirers initially lose then break even, and the combined value change is positive.")
add(T, "The main purpose of organizing a *sale by auction* in M&A is to:",
    ["Conceal the seller's private information",
     "Force bidders to reveal their true preferences/valuations and reduce information asymmetry",
     "Guarantee the buyer avoids the winner's curse", "Eliminate due diligence"],
    [1], "Ch14 \u00a714.5: auctions make bidders disclose valuations and reduce information asymmetry.")
add(T, "Order the auction stages: (1) due diligence in a data room; (2) information memorandum + indicative bid; (3) binding bid + SPA; (4) exclusivity with the most sensitive info.",
    ["2 \u2192 1 \u2192 3 \u2192 4", "1 \u2192 2 \u2192 3 \u2192 4", "2 \u2192 3 \u2192 1 \u2192 4", "4 \u2192 3 \u2192 2 \u2192 1"],
    [0], "Ch14 \u00a714.5: first stage IM + indicative bid \u2192 second stage due diligence/data room \u2192 binding bid/SPA \u2192 third-stage exclusivity.")
add(T, "The *winner's curse* is explained partly by managerial:",
    ["Risk aversion", "Overconfidence/hubris, leading to value-destroying acquisitions",
     "Loss aversion", "Satisficing"],
    [1], "Ch14 \u00a714.6: hubris/overconfidence makes winners overpay and destroy value.")
add(T, "Hidden-information solution: with a *single* interested buyer vs *multiple* interested buyers, the notes recommend:",
    ["Single \u2192 IPO; Multiple \u2192 joint venture",
     "Single \u2192 joint venture; Multiple \u2192 Initial Public Offering",
     "Both \u2192 break-up fee", "Both \u2192 MAC clause"],
    [1], "Ch14 \u00a714.7: a single buyer \u2192 JV to equalize information; multiple buyers \u2192 IPO.")
add(T, "A *Material Adverse Change (MAC)* clause lets the buyer walk away when:",
    ["Any exogenous, generic-nature risk materializes",
     "An endogenous (moral-hazard) risk materializes, but not a purely exogenous one",
     "The seller's share price rises", "The auction is sealed-bid"],
    [1], "Ch14 \u00a714.8: MAC clauses cover endogenous (moral hazard) risk, not generic exogenous risk.")
add(T, "A *break-up fee* is primarily a solution to:",
    ["Adverse selection in IPOs",
     "Hold-up from high asset specificity + opportunism \u2014 a credible commitment obliging the party that walks away to pay",
     "The free-rider problem in teams", "Bounded rationality"],
    [1], "Ch14 \u00a714.9: a break-up fee is a credible commitment against hold-up under high asset specificity.")

# ===== Ch15 — Hybrid forms =====
T = "Chapter 15 — Hybrid Forms"
add(T, "Hybrid forms are *most efficient* (lowest transaction costs) when asset specificity is:",
    ["Very low", "Intermediate", "Very high", "Irrelevant"],
    [1], "Ch15 \u00a715.1: hybrids minimize transaction costs at intermediate levels of asset specificity.")
add(T, "(Select TWO) In co-makership the traded assets have high asset specificity, so why do suppliers accept the vulnerability?",
    ["Long-term contracts protect against opportunism",
     "Opportunism never occurs in practice",
     "The buyer's benefits from future cooperation outweigh the gains from opportunism, and opportunism harms reputation",
     "Asset specificity is actually zero"],
    [0, 2], "Ch15 \u00a715.2: long-term contracts + future-cooperation benefits + reputation effects protect the supplier.")
add(T, "A joint venture (JV) is the preferred form when, among others:",
    ["Assets are easily transacted on the market at low cost",
     "The opportunity needs assets from two firms, those assets are intangible (know-how, contacts) and costly to trade due to opportunism, and vertical integration is not viable",
     "One firm can simply buy the other's tangible assets cheaply",
     "There is no need for mutual trust"],
    [1], "Ch15 \u00a715.3: JVs pool intangible assets that the market would price too highly, when integration is not viable.")
add(T, "An *associative/horizontal* business group differs from a *hierarchical/vertical* one in that:",
    ["It has a central holding company controlling all firms",
     "It has no central holding company \u2014 a loose confederation linked by ties, coordinated by mutual adjustment + standardization of norms",
     "It is controlled by a single investor via a pyramid",
     "It uses only direct supervision"],
    [1], "Ch15 \u00a715.4: associative groups are loose confederations; hierarchical groups are controlled by a single investor (often a pyramid).")
add(T, "(Select TWO) Mechanisms that let an investor control firms worth more than their wealth, separating ownership and control, include:",
    ["Pyramids", "Co-makership", "Dual-class equity / differential voting rights", "Information memoranda"],
    [0, 2], "Ch15 \u00a715.4: pyramids and dual-class shares separate control from cash-flow rights.")
add(T, "*Tunneling* vs *propping*:",
    ["Tunneling = supporting weak firms; Propping = extracting value",
     "Tunneling = transferring value from low-cash-flow-right firms to high-cash-flow-right firms; Propping = controlling owners support struggling firms for their own benefit",
     "Both mean issuing new equity",
     "Both reduce the controlling owner's benefits"],
    [1], "Ch15 \u00a715.4: tunneling extracts value toward high-cash-flow-right firms; propping is negative tunneling (support).")
add(T, "The *administrative efficiency thesis* for franchising holds that:",
    ["Franchising exists only because the franchisor lacks capital/managers",
     "Franchising is a more efficient governance structure than pure hierarchy or pure market \u2014 letting owners monitor operators, reduce shirking/free-riding and preserve the brand",
     "Franchising eliminates standardization",
     "Franchising is always inferior to company ownership"],
    [1], "Ch15 \u00a715.6: the administrative-efficiency thesis stresses governance efficiency; option A is the resource-scarcity thesis.")
add(T, "Informal networks are coordinated mainly by:",
    ["The price mechanism alone",
     "Trust, mutual adjustment and standardization of norms (firms still transact on the market); important where dispute-settling institutions are weak",
     "A pyramid holding company", "Standardization of outputs by HQ"],
    [1], "Ch15 \u00a715.5: informal networks rest on trust/interlocking directorates and matter where institutions are underdeveloped.")

# ===== Ch16 — Corporate governance =====
T = "Chapter 16 — Corporate Governance"
add(T, "Corporate governance is defined as:",
    ["The system by which business corporations are directed and controlled",
     "The price mechanism for shares", "A synonym for competitive strategy",
     "The market for intermediate goods"],
    [0], "Ch16 \u00a716.1: governance is the system by which corporations are directed and controlled.")
add(T, "The *free-cash-flow* agency problem is that:",
    ["Managers always return all free cash flow to shareholders",
     "Free cash flow should be returned to shareholders, but the CEO may wish to retain it to diversify into other businesses",
     "Shareholders are more risk-averse than the CEO",
     "Managers have an infinite time horizon"],
    [1], "Ch16 \u00a716.1: free cash flow ought to be paid out, but managers prefer to retain it for empire-building.")
add(T, "The 'different time horizons' problem can bias managers toward:",
    ["Long-term NPV-positive projects",
     "Projects with high short-term accounting returns even if NPV is negative",
     "Returning cash to shareholders", "Reducing on-the-job consumption"],
    [1], "Ch16 \u00a716.1: managers' limited tenure biases them to short-term accounting gains over long-term value.")
add(T, "Offering the manager an incentive contract is a:",
    ["Market solution to reduce information asymmetry",
     "Organizational solution to align interests",
     "External monitoring mechanism", "Market solution to align interests"],
    [1], "Ch16 \u00a716.1: incentive contracts are the organizational solution for aligning interests; markets for labour/control are the market solution.")
add(T, "Giving a manager *too many* shares can cause:",
    ["Managerial entrenchment", "The free-rider problem",
     "Adverse selection", "The winner's curse"],
    [0], "Ch16 \u00a716.3: excessive share ownership can entrench managers.")
add(T, "*Relative performance evaluation* rewards managers based on:",
    ["Absolute net profit only",
     "Performance measured against a reference group of similar companies (filtering out external factors)",
     "The number of shares outstanding", "Tenure"],
    [1], "Ch16 \u00a716.3: benchmarking against a peer group strips out macro/external factors managers do not control.")
add(T, "In the *two-tier* board system, the supervisory board:",
    ["Consists of executive directors who run the firm",
     "Consists exclusively of outside members, is elected by the employees, and monitors/advises the executive board",
     "Is the same as a one-tier board", "Reports to the CEO"],
    [1], "Ch16 \u00a716.4: the supervisory board (outside members, elected by employees) monitors and advises the executive board.")
add(T, "For auditors to be effective monitors, the notes stress that they must:",
    ["Also do consulting for the firms they audit",
     "Be independent \u2014 no consulting for audited firms \u2014 and report to boards/audit committees rather than to CEOs",
     "Report directly to the CEO", "Hold large equity stakes"],
    [1], "Ch16 \u00a716.5: auditor independence requires no consulting for audited firms and reporting to the board/audit committee.")
add(T, "(Select TWO) Which markets align managers' interests with shareholders'?",
    ["Market for corporate control (takeover threat)", "Product market (forces cost minimization)",
     "The endowment market", "The data room"],
    [0, 1], "Ch16 \u00a716.6: the product, managerial-labour, stock and corporate-control markets all align managers with shareholders.")
add(T, "In a *network-oriented* (vs market-oriented) governance system:",
    ["Shareholding is widely dispersed and managers are disciplined mainly by hostile takeovers",
     "Listed firms have one or a few large blockholders who sit on the board and discipline managers through monitoring",
     "Insider-trading laws are extremely strict",
     "No shareholder holds a controlling block"],
    [1], "Ch16 \u00a716.7: network-oriented systems feature concentrated blockholders/monitoring; the other options describe market-oriented systems.")

assert len(Q) == 100, f"expected 100, got {len(Q)}"

# ---------------------------------------------------------------------------
# Build HTML
# ---------------------------------------------------------------------------
LETTERS = "ABCDEFG"

def esc(s):
    return html.escape(s)

def fmt(s):
    # escape, then turn *emphasis* into italics
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", html.escape(s))

def exam_html():
    parts = ['<div class="cover">',
             '<div class="kicker">BUSINESS &middot; MARKETS &amp; ORGANIZATIONS</div>',
             '<h1>Practice Exam</h1>',
             '<div class="sub">100 multiple-choice questions &middot; open-book level (hard)</div>',
             '</div>']
    parts.append('<div class="instr">')
    parts.append('<h3>Instructions</h3>'
                 '<ul>'
                 '<li>100 questions, grouped by chapter for easy reference. In the real exam the order is randomized.</li>'
                 '<li>Most questions have <b>one</b> correct answer. Questions needing more are marked <b>(Select TWO)</b> or <b>(Select THREE)</b>.</li>'
                 '<li>No marks are deducted for wrong answers, so never leave a question blank.</li>'
                 '<li>Some stems ask for the <b>EXCEPT</b> / <b>INCORRECT</b> option \u2014 read carefully.</li>'
                 '<li>Full worked answers with chapter/section references start after question 100.</li>'
                 '</ul>')
    parts.append('</div>')

    current = None
    for i, item in enumerate(Q, 1):
        if item["topic"] != current:
            current = item["topic"]
            cls = "topic first" if i == 1 else "topic"
            parts.append(f'<div class="{cls}">{esc(current)}</div>')
        tag = ' <span class="multi">(Select TWO)</span>' if len(item["ans"]) == 2 else (
              ' <span class="multi">(Select THREE)</span>' if len(item["ans"]) == 3 else '')
        stem = item["q"]
        for marker in ("(Select TWO) ", "(Select THREE) ", "(Select TWO)", "(Select THREE)"):
            stem = stem.replace(marker, "")
        parts.append('<div class="q">')
        parts.append(f'<p class="stem"><span class="qn">{i}.</span> {fmt(stem)}{tag}</p>')
        for j, opt in enumerate(item["opts"]):
            parts.append(f'<p class="opt"><b class="ol">{LETTERS[j]}.</b> {fmt(opt)}</p>')
        parts.append('</div>')
    return "\n".join(parts)

def answers_html():
    parts = ['<div class="akhead"><h2>Answer Key &amp; Explanations</h2>'
             '<p class="aksub">Correct option(s) in bold, with the reasoning and the note reference.</p></div>']
    current = None
    for i, item in enumerate(Q, 1):
        if item["topic"] != current:
            current = item["topic"]
            parts.append(f'<div class="atopic">{esc(current)}</div>')
        letters = ", ".join(LETTERS[k] for k in item["ans"])
        parts.append('<div class="a">')
        parts.append(f'<p class="aline"><span class="aqn">{i}.</span> '
                     f'<span class="acorrect">{letters}</span> &mdash; {esc(item["exp"])}</p>')
        parts.append('</div>')
    return "\n".join(parts)

def clean_stem(q):
    stem = q
    for marker in ("(Select TWO) ", "(Select THREE) ", "(Select TWO)", "(Select THREE)"):
        stem = stem.replace(marker, "")
    return stem

def multi_tag(n):
    if n == 2:
        return ' <span class="multi">(Select TWO)</span>'
    if n == 3:
        return ' <span class="multi">(Select THREE)</span>'
    return ""

def chapter_slug(topic):
    m = re.search(r"Chapter\s+(\d+)", topic)
    return f"ch{m.group(1)}" if m else re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")

def exam_html_web():
    parts = []
    seen = []
    for item in Q:
        if item["topic"] not in seen:
            seen.append(item["topic"])
    nav = ['<nav class="toc" aria-label="Chapters">',
           '<p class="toc-title">Jump to chapter</p>',
           '<div class="toc-links">']
    for topic in seen:
        slug = chapter_slug(topic)
        short = re.sub(r"^Chapter \d+ — ", "", topic)
        nav.append(f'<a href="#{slug}">{esc(short)}</a>')
    nav.append('<a class="toc-answers" href="#answers">Full answer key</a>')
    nav.append('</div></nav>')
    parts.extend(nav)
    parts.append('<section id="questions" class="section">')
    current = None
    for i, item in enumerate(Q, 1):
        if item["topic"] != current:
            current = item["topic"]
            slug = chapter_slug(current)
            parts.append(f'<h2 class="chapter" id="{slug}">{esc(current)}</h2>')
        stem = clean_stem(item["q"])
        tag = multi_tag(len(item["ans"]))
        correct = ",".join(str(x) for x in item["ans"])
        pick = len(item["ans"])
        parts.append(
            f'<article class="question" id="q{i}" data-correct="{correct}" data-pick="{pick}">'
        )
        parts.append('<div class="q-meta">')
        parts.append(f'<span class="q-num">{i}</span>')
        parts.append('<span class="q-status" aria-label="Not answered"></span>')
        parts.append('</div>')
        parts.append(f'<p class="stem">{fmt(stem)}{tag}</p>')
        parts.append('<ul class="options" role="group">')
        for j, opt in enumerate(item["opts"]):
            parts.append(
                f'<li><button type="button" class="opt-btn" data-idx="{j}" aria-pressed="false">'
                f'<span class="ol">{LETTERS[j]}.</span><span class="opt-text">{fmt(opt)}</span>'
                f'<span class="opt-icon" aria-hidden="true"></span></button></li>'
            )
        parts.append('</ul>')
        if pick > 1:
            parts.append(
                f'<div class="multi-bar"><span class="pick-count">0 / {pick} selected</span>'
                f'<button type="button" class="btn-check" disabled>Check answer</button></div>'
            )
        parts.append(f'<div class="feedback" role="status" aria-live="polite"></div>')
        parts.append(f'<div class="explain">{esc(item["exp"])}</div>')
        parts.append('<button type="button" class="btn-retry">Try again</button>')
        parts.append('</article>')
    parts.append('</section>')
    return "\n".join(parts)

def answers_html_web():
    parts = ['<section id="answers" class="section answers">',
             '<header class="akhead">',
             '<h2>Answer Key &amp; Explanations</h2>',
             '<p class="aksub">Correct option(s) highlighted. Click a question number to jump back.</p>',
             '</header>']
    current = None
    for i, item in enumerate(Q, 1):
        if item["topic"] != current:
            current = item["topic"]
            parts.append(f'<h3 class="atopic">{esc(current)}</h3>')
        letters = ", ".join(LETTERS[k] for k in item["ans"])
        parts.append(f'<article class="answer" id="a{i}">')
        parts.append(f'<p class="aline">'
                     f'<a class="back" href="#q{i}">{i}</a> '
                     f'<span class="acorrect">{letters}</span> '
                     f'<span class="exp">&mdash; {esc(item["exp"])}</span></p>')
        parts.append('</article>')
    parts.append('</section>')
    return "\n".join(parts)

WEB_CSS = """
:root {
  --navy: #1f335c;
  --teal: #2e8b8b;
  --teal-d: #247878;
  --amber: #b06a00;
  --green: #1a7f4b;
  --green-bg: #e8f7ef;
  --red: #c0392b;
  --red-bg: #fdecea;
  --ink: #14171b;
  --muted: #5a5f66;
  --bg: #eef1f6;
  --card: #ffffff;
  --border: #dde3ec;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.5;
}
.topbar {
  position: sticky;
  top: 0;
  z-index: 200;
  background: var(--navy);
  color: #fff;
  padding: 0.6rem 1rem;
  box-shadow: 0 2px 16px rgba(0,0,0,.18);
}
.topbar-inner {
  max-width: 820px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.65rem 1rem;
}
.topbar-title { font-weight: 700; font-size: 0.88rem; flex: 1 1 180px; }
.score-panel { flex: 2 1 220px; min-width: 180px; }
.score-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 0.78rem;
  margin-bottom: 0.25rem;
  color: #c8d4e8;
}
.score-row strong { color: #fff; font-size: 1rem; }
.progress-track {
  height: 6px;
  background: rgba(255,255,255,.15);
  border-radius: 999px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, var(--teal), #5ec4c4);
  border-radius: 999px;
  transition: width .35s ease;
}
.topbar-actions { display: flex; gap: 0.4rem; flex-wrap: wrap; }
.btn {
  border: none;
  border-radius: 6px;
  padding: 0.4rem 0.75rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  font-family: inherit;
  transition: filter .15s, transform .1s;
}
.btn:active { transform: scale(.97); }
.btn-primary { background: var(--teal); color: #fff; }
.btn-primary:hover { filter: brightness(1.1); }
.btn-ghost { background: rgba(255,255,255,.12); color: #fff; }
.btn-ghost:hover { background: rgba(255,255,255,.22); }
.btn-danger { background: rgba(255,255,255,.1); color: #ffb4b4; border: 1px solid rgba(255,255,255,.2); }
.wrap { max-width: 820px; margin: 0 auto; padding: 1.25rem 1rem 3rem; }
.hero {
  background: linear-gradient(135deg, var(--navy) 0%, #2a4a7a 100%);
  color: #fff;
  border-radius: 12px;
  padding: 1.5rem 1.35rem;
  margin-bottom: 1rem;
}
.hero .kicker { color: #8ecfd0; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; }
.hero h1 { margin: 0.3rem 0 0.2rem; font-size: 1.7rem; }
.hero .sub { color: #c8d4e8; font-size: 0.92rem; margin: 0; }
.instr {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.9rem 1.1rem;
  margin-bottom: 1rem;
  font-size: 0.88rem;
  color: var(--muted);
}
.instr strong { color: var(--navy); }
.filter-bar {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}
.filter-bar .btn-filter {
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
}
.filter-bar .btn-filter.active {
  background: var(--navy);
  color: #fff;
  border-color: var(--navy);
}
.toc {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.9rem 1.1rem;
  margin-bottom: 1.25rem;
}
.toc-title { margin: 0 0 0.55rem; font-size: 0.75rem; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
.toc-links { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.toc a {
  font-size: 0.78rem;
  padding: 0.28rem 0.6rem;
  border-radius: 999px;
  background: #eef2f8;
  color: var(--navy);
  text-decoration: none;
  font-weight: 600;
}
.toc a:hover { background: #dce6f2; }
.toc-answers { background: #fff3e0 !important; color: var(--amber) !important; }
.chapter {
  margin: 1.75rem 0 0.85rem;
  padding: 0.6rem 1rem;
  background: var(--navy);
  color: #fff;
  border-radius: 8px;
  font-size: 1rem;
}
.question {
  background: var(--card);
  border: 2px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.1rem 0.85rem;
  margin-bottom: 0.75rem;
  transition: border-color .25s, box-shadow .25s;
}
.question.unanswered { border-color: var(--border); }
.question.answered-correct {
  border-color: var(--green);
  box-shadow: 0 0 0 1px var(--green), 0 4px 14px rgba(26,127,75,.12);
}
.question.answered-wrong {
  border-color: var(--red);
  box-shadow: 0 0 0 1px var(--red), 0 4px 14px rgba(192,57,43,.1);
}
.question.hidden-q { display: none; }
.q-meta { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.45rem; }
.q-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.75rem;
  height: 1.75rem;
  background: var(--navy);
  color: #fff;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 700;
}
.q-status {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  background: #eef2f8;
  color: var(--muted);
}
.question.answered-correct .q-status { background: var(--green-bg); color: var(--green); }
.question.answered-wrong .q-status { background: var(--red-bg); color: var(--red); }
.stem { margin: 0 0 0.75rem; font-size: 0.96rem; font-weight: 500; }
.multi { color: var(--amber); font-weight: 700; font-size: 0.82rem; }
.options { list-style: none; margin: 0; padding: 0; }
.options li { margin: 0.35rem 0; }
.opt-btn {
  width: 100%;
  display: flex;
  align-items: flex-start;
  gap: 0.35rem;
  text-align: left;
  padding: 0.65rem 0.75rem;
  border: 2px solid var(--border);
  border-radius: 8px;
  background: #fafbfc;
  color: var(--ink);
  font-size: 0.9rem;
  line-height: 1.4;
  cursor: pointer;
  font-family: inherit;
  transition: border-color .15s, background .15s, transform .1s;
}
.opt-btn:hover:not(:disabled) {
  border-color: var(--teal);
  background: #f0faf9;
}
.opt-btn:active:not(:disabled) { transform: scale(.995); }
.opt-btn:disabled { cursor: default; }
.opt-btn.selected {
  border-color: var(--teal);
  background: #e6f5f5;
  box-shadow: inset 0 0 0 1px var(--teal);
}
.opt-btn.correct {
  border-color: var(--green) !important;
  background: var(--green-bg) !important;
  color: #0d4d2c;
}
.opt-btn.wrong {
  border-color: var(--red) !important;
  background: var(--red-bg) !important;
  color: #7a1f18;
}
.opt-btn.missed {
  border-color: var(--green);
  background: var(--green-bg);
  border-style: dashed;
}
.ol { font-weight: 700; color: var(--teal); flex-shrink: 0; }
.opt-text { flex: 1; }
.opt-icon {
  flex-shrink: 0;
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 800;
  opacity: 0;
  transition: opacity .2s;
}
.opt-btn.correct .opt-icon,
.opt-btn.wrong .opt-icon,
.opt-btn.missed .opt-icon { opacity: 1; }
.opt-btn.correct .opt-icon { background: var(--green); color: #fff; }
.opt-btn.correct .opt-icon::after { content: "✓"; }
.opt-btn.wrong .opt-icon { background: var(--red); color: #fff; }
.opt-btn.wrong .opt-icon::after { content: "✗"; }
.opt-btn.missed .opt-icon { background: var(--green); color: #fff; border: 2px dashed var(--green); }
.opt-btn.missed .opt-icon::after { content: "✓"; }
.multi-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-top: 0.65rem;
  padding-top: 0.5rem;
  border-top: 1px dashed var(--border);
}
.pick-count { font-size: 0.82rem; color: var(--muted); font-weight: 600; }
.btn-check {
  padding: 0.45rem 1rem;
  border: none;
  border-radius: 8px;
  background: var(--navy);
  color: #fff;
  font-weight: 700;
  font-size: 0.82rem;
  cursor: pointer;
  font-family: inherit;
}
.btn-check:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-check:not(:disabled):hover { filter: brightness(1.12); }
.feedback {
  margin-top: 0.75rem;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  display: none;
  animation: fadeUp .3s ease;
}
.feedback.show { display: block; }
.feedback.ok { background: var(--green-bg); color: var(--green); border-left: 4px solid var(--green); }
.feedback.bad { background: var(--red-bg); color: var(--red); border-left: 4px solid var(--red); }
.explain {
  margin-top: 0.55rem;
  padding: 0.65rem 0.85rem;
  background: #f7f9fc;
  border-radius: 8px;
  border-left: 3px solid var(--teal);
  font-size: 0.84rem;
  color: #333;
  line-height: 1.45;
  display: none;
  animation: fadeUp .35s ease .05s both;
}
.explain.show { display: block; }
.btn-retry {
  margin-top: 0.55rem;
  padding: 0.3rem 0.65rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: #fff;
  color: var(--muted);
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  display: none;
}
.btn-retry.show { display: inline-block; }
.btn-retry:hover { border-color: var(--teal); color: var(--teal); }
.question.shake { animation: shake .4s ease; }
@keyframes shake {
  0%,100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes pop {
  0% { transform: scale(1); }
  50% { transform: scale(1.015); }
  100% { transform: scale(1); }
}
.question.answered-correct { animation: pop .35s ease; }
.answers { margin-top: 2rem; }
body.hide-answers .answers { display: none; }
.akhead {
  background: var(--teal);
  color: #fff;
  border-radius: 10px;
  padding: 1rem 1.15rem;
  margin-bottom: 1rem;
}
.akhead h2 { margin: 0; font-size: 1.2rem; }
.aksub { margin: 0.35rem 0 0; font-size: 0.85rem; opacity: 0.92; }
.atopic {
  margin: 1.15rem 0 0.45rem;
  padding-left: 0.75rem;
  border-left: 4px solid var(--teal);
  color: var(--navy);
  font-size: 0.95rem;
}
.answer {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.55rem 0.8rem;
  margin-bottom: 0.4rem;
}
.aline { margin: 0; font-size: 0.86rem; }
.back {
  display: inline-block;
  min-width: 1.5rem;
  text-align: center;
  background: var(--navy);
  color: #fff !important;
  border-radius: 4px;
  padding: 0.08rem 0.3rem;
  text-decoration: none;
  font-weight: 700;
  font-size: 0.78rem;
  margin-right: 0.3rem;
}
.acorrect { font-weight: 700; color: var(--amber); }
.exp { color: #333; }
footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.78rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}
@media (max-width: 520px) {
  .topbar-inner { flex-direction: column; align-items: stretch; }
  .score-panel { order: 2; }
}
@media print {
  .topbar, .filter-bar, .toc, .btn-retry, .multi-bar, .back { display: none !important; }
  body { background: #fff; }
  .question { break-inside: avoid; }
}
"""

WEB_JS = """
(function () {
  var LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var questions = Array.prototype.slice.call(document.querySelectorAll(".question"));
  var total = questions.length;
  var state = {}; // id -> { answered, correct, selected:Set }

  var elAnswered = document.getElementById("statAnswered");
  var elCorrect = document.getElementById("statCorrect");
  var elPct = document.getElementById("statPct");
  var elFill = document.getElementById("progressFill");

  function parseCorrect(card) {
    return card.dataset.correct.split(",").map(Number);
  }

  function fmtLetters(idxs) {
    return idxs.map(function (i) { return LETTERS[i]; }).join(", ");
  }

  function setsEqual(a, b) {
    if (a.size !== b.size) return false;
    var ok = true;
    a.forEach(function (v) { if (!b.has(v)) ok = false; });
    return ok;
  }

  function updateScore() {
    var answered = 0, correct = 0;
    questions.forEach(function (card) {
      var s = state[card.id];
      if (s && s.answered) {
        answered++;
        if (s.correct) correct++;
      }
    });
    if (elAnswered) elAnswered.textContent = answered;
    if (elCorrect) elCorrect.textContent = correct;
    if (elPct) elPct.textContent = answered ? Math.round(correct / answered * 100) + "%" : "—";
    if (elFill) elFill.style.width = (answered / total * 100) + "%";
  }

  function lockCard(card, locked) {
    card.querySelectorAll(".opt-btn").forEach(function (btn) {
      btn.disabled = locked;
    });
    var chk = card.querySelector(".btn-check");
    if (chk) chk.disabled = locked || chk.disabled;
  }

  function resetCard(card) {
    var pick = parseInt(card.dataset.pick, 10);
    state[card.id] = { answered: false, correct: false, selected: new Set() };
    card.classList.remove("answered-correct", "answered-wrong", "shake");
    card.classList.add("unanswered");
    var status = card.querySelector(".q-status");
    status.textContent = "";
    status.removeAttribute("aria-label");
    card.querySelectorAll(".opt-btn").forEach(function (btn) {
      btn.className = "opt-btn";
      btn.disabled = false;
      btn.setAttribute("aria-pressed", "false");
    });
    var fb = card.querySelector(".feedback");
    fb.className = "feedback";
    fb.textContent = "";
    var ex = card.querySelector(".explain");
    ex.classList.remove("show");
    var retry = card.querySelector(".btn-retry");
    retry.classList.remove("show");
    var bar = card.querySelector(".multi-bar");
    if (bar) {
      var cnt = bar.querySelector(".pick-count");
      cnt.textContent = "0 / " + pick + " selected";
      var chk = bar.querySelector(".btn-check");
      chk.disabled = true;
    }
    lockCard(card, false);
    applyFilter();
    updateScore();
  }

  function revealGrades(card, selected, correctSet, isCorrect) {
    card.querySelectorAll(".opt-btn").forEach(function (btn) {
      var idx = parseInt(btn.dataset.idx, 10);
      btn.classList.remove("selected");
      if (correctSet.has(idx)) {
        btn.classList.add(selected.has(idx) ? "correct" : "missed");
      } else if (selected.has(idx)) {
        btn.classList.add("wrong");
      }
    });
  }

  function grade(card, selected) {
    if (state[card.id] && state[card.id].answered) return;
    var correctSet = new Set(parseCorrect(card));
    var isCorrect = setsEqual(selected, correctSet);
    state[card.id] = { answered: true, correct: isCorrect, selected: selected };

    card.classList.remove("unanswered");
    card.classList.add(isCorrect ? "answered-correct" : "answered-wrong");
    if (!isCorrect) {
      card.classList.add("shake");
      setTimeout(function () { card.classList.remove("shake"); }, 450);
    }

    var status = card.querySelector(".q-status");
    status.textContent = isCorrect ? "Correct" : "Incorrect";
    status.setAttribute("aria-label", isCorrect ? "Answered correctly" : "Answered incorrectly");

    revealGrades(card, selected, correctSet, isCorrect);

    var fb = card.querySelector(".feedback");
    fb.className = "feedback show " + (isCorrect ? "ok" : "bad");
    if (isCorrect) {
      fb.textContent = "Correct! Well done.";
    } else {
      fb.textContent = "Not quite — correct answer: " + fmtLetters(Array.from(correctSet).sort());
    }

    card.querySelector(".explain").classList.add("show");
    card.querySelector(".btn-retry").classList.add("show");
    lockCard(card, true);
    updateScore();
    applyFilter();
  }

  questions.forEach(function (card) {
    resetCard(card);
    var pick = parseInt(card.dataset.pick, 10);
    var isMulti = pick > 1;

    card.querySelectorAll(".opt-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (state[card.id].answered) return;
        var idx = parseInt(btn.dataset.idx, 10);

        if (isMulti) {
          var sel = state[card.id].selected;
          if (sel.has(idx)) { sel.delete(idx); btn.classList.remove("selected"); btn.setAttribute("aria-pressed", "false"); }
          else {
            if (sel.size >= pick) return;
            sel.add(idx); btn.classList.add("selected"); btn.setAttribute("aria-pressed", "true");
          }
          var bar = card.querySelector(".multi-bar");
          bar.querySelector(".pick-count").textContent = sel.size + " / " + pick + " selected";
          bar.querySelector(".btn-check").disabled = sel.size !== pick;
        } else {
          var single = new Set([idx]);
          btn.classList.add("selected");
          grade(card, single);
        }
      });
    });

    var chk = card.querySelector(".btn-check");
    if (chk) {
      chk.addEventListener("click", function () {
        if (state[card.id].answered) return;
        grade(card, new Set(state[card.id].selected));
      });
    }

    card.querySelector(".btn-retry").addEventListener("click", function () {
      resetCard(card);
    });
  });

  /* Filters */
  var currentFilter = "all";
  function applyFilter() {
    questions.forEach(function (card) {
      var s = state[card.id];
      var show = true;
      if (currentFilter === "unanswered") show = !s.answered;
      else if (currentFilter === "wrong") show = s.answered && !s.correct;
      else if (currentFilter === "correct") show = s.answered && s.correct;
      card.classList.toggle("hidden-q", !show);
    });
  }

  document.querySelectorAll(".btn-filter").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll(".btn-filter").forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      currentFilter = btn.dataset.filter;
      applyFilter();
    });
  });

  document.getElementById("btnResetAll").addEventListener("click", function () {
    if (!confirm("Reset all " + total + " questions?")) return;
    questions.forEach(resetCard);
  });

  var toggleBtn = document.getElementById("toggleAnswers");
  toggleBtn.addEventListener("click", function () {
    document.body.classList.toggle("hide-answers");
    toggleBtn.textContent = document.body.classList.contains("hide-answers")
      ? "Show full answer key" : "Hide full answer key";
  });
})();
"""

def export_html():
    body = exam_html_web() + answers_html_web()
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Business: Markets &amp; Organizations — Interactive Practice Exam</title>
<style>{WEB_CSS}</style>
</head>
<body class="hide-answers">
<header class="topbar">
  <div class="topbar-inner">
    <div class="topbar-title">Business · Markets &amp; Organizations</div>
    <div class="score-panel">
      <div class="score-row">
        <span>Answered <strong><span id="statAnswered">0</span>/{len(Q)}</strong></span>
        <span>Correct <strong id="statCorrect">0</strong></span>
        <span>Accuracy <strong id="statPct">—</strong></span>
      </div>
      <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
    </div>
    <div class="topbar-actions">
      <button type="button" class="btn btn-primary" id="toggleAnswers">Show full answer key</button>
      <button type="button" class="btn btn-danger" id="btnResetAll">Reset all</button>
    </div>
  </div>
</header>
<main class="wrap">
  <header class="hero">
    <div class="kicker">Interactive practice exam</div>
    <h1>100 MCQs — click to answer</h1>
    <p class="sub">Instant feedback · explanations · score tracker</p>
  </header>
  <div class="instr">
    <strong>How it works:</strong> Click an option for single-answer questions — you get instant feedback.
    For <em>(Select TWO/THREE)</em> questions, pick all required options then press <strong>Check answer</strong>.
    Wrong answers show the correct option(s) and a short explanation from your notes.
  </div>
  <div class="filter-bar">
    <button type="button" class="btn-filter active" data-filter="all">All questions</button>
    <button type="button" class="btn-filter" data-filter="unanswered">Unanswered</button>
    <button type="button" class="btn-filter" data-filter="wrong">Got wrong</button>
    <button type="button" class="btn-filter" data-filter="correct">Got right</button>
  </div>
  {body}
  <footer>Interactive exam · {len(Q)} questions · open in any browser (works offline on USB)</footer>
</main>
<script>{WEB_JS}</script>
</body>
</html>"""
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Saved {HTML_OUT} + index.html: {len(Q)} interactive questions")

CSS = """
* { font-family: sans-serif; }
h1 { font-size: 34pt; color: #1f335c; margin: 4pt 0; }
h2 { font-size: 19pt; color: #ffffff; margin: 0; }
h3 { font-size: 12.5pt; color: #1f335c; margin: 0 0 4pt 0; }
.cover { margin-top: 40pt; margin-bottom: 6pt; }
.kicker { font-size: 11pt; color: #2e8b8b; font-weight: bold; letter-spacing: 1pt; }
.sub { font-size: 12.5pt; color: #5a5f66; margin-top: 2pt; }
.instr { background-color: #eef2f8; padding: 9pt 12pt; margin: 8pt 0 14pt 0; }
.instr ul { margin: 0; padding-left: 14pt; }
.instr li { font-size: 9.7pt; color: #2b2f36; line-height: 1.45; margin-bottom: 2pt; }
.topic { font-size: 12.5pt; font-weight: bold; color: #ffffff; background-color: #1f335c;
         padding: 5pt 9pt; margin: 15pt 0 8pt 0; }
.topic.first { margin-top: 4pt; }
.q { margin: 0 0 9pt 0; }
.stem { font-size: 10.3pt; color: #14171b; line-height: 1.4; margin: 0 0 3pt 0; }
.qn { font-weight: bold; color: #1f335c; }
.multi { color: #b06a00; font-weight: bold; font-size: 9pt; }
.opt { font-size: 9.8pt; color: #23272d; margin: 1pt 0 1pt 18pt; line-height: 1.35; }
.ol { font-weight: bold; color: #2e8b8b; }
.akhead { background-color: #2e8b8b; padding: 8pt 10pt; margin: 0 0 10pt 0; }
.aksub { color: #eafafa; font-size: 9.5pt; margin: 3pt 0 0 0; }
.atopic { font-size: 11.5pt; font-weight: bold; color: #1f335c;
          border-left: 4pt solid #2e8b8b; padding-left: 7pt; margin: 12pt 0 5pt 0; }
.a { margin: 0 0 4pt 0; }
.aline { font-size: 9.5pt; color: #23272d; line-height: 1.4; margin: 0; }
.aqn { font-weight: bold; color: #1f335c; }
.acorrect { font-weight: bold; color: #b06a00; }
"""

def render(writer, html_str, mediabox, where):
    story = fitz.Story(html=html_str, user_css=CSS)
    more = 1
    while more:
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()

def main():
    mediabox = fitz.paper_rect("letter")
    where = mediabox + (54, 54, -54, -56)
    writer = fitz.DocumentWriter(OUT)
    render(writer, exam_html(), mediabox, where)
    render(writer, answers_html(), mediabox, where)
    writer.close()

    # post-process: footers, page numbers, metadata, bookmarks
    doc = fitz.open(OUT)
    n = doc.page_count
    ak_page = None
    for i in range(n):
        p = doc[i]
        if ak_page is None and p.search_for("Answer Key & Explanations"):
            ak_page = i
        # thin top accent rule
        p.draw_line(fitz.Point(54, 44), fitz.Point(mediabox.x1 - 54, 44),
                    color=(0.18, 0.34, 0.55), width=1.1)
        foot = f"Business \u00b7 Markets & Organizations \u2014 Practice Exam"
        p.insert_text((54, mediabox.y1 - 30), foot, fontname="helv", fontsize=8,
                      color=(0.45, 0.48, 0.52))
        pn = f"{i + 1} / {n}"
        w = fitz.get_text_length(pn, fontname="helv", fontsize=8)
        p.insert_text((mediabox.x1 - 54 - w, mediabox.y1 - 30), pn, fontname="helv",
                      fontsize=8, color=(0.45, 0.48, 0.52))
    toc = [[1, "Practice Exam (Questions)", 1]]
    if ak_page is not None:
        toc.append([1, "Answer Key & Explanations", ak_page + 1])
    doc.set_toc(toc)
    doc.set_metadata({"title": "Business: Markets & Organizations \u2014 Practice Exam (100 MCQs)",
                      "subject": "Open-book practice exam with answer key",
                      "keywords": "MCQ, exam, markets, organizations"})
    doc.saveIncr()
    print(f"Saved {OUT}: {n} pages, {len(Q)} questions, answer key on page {ak_page+1 if ak_page else '?'}")
    doc.close()
    export_html()

if __name__ == "__main__":
    main()
