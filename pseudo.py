from bird import *

def generate_alleles(num_loci):

    zer_one_locus = [[0,1] for i in range(num_loci)]
    zer_zer_locus = [[0,0] for i in range(num_loci)]

    f_alls, m_alls = dict(), dict()

    f_alls['x'] = zer_one_locus
    f_alls['p'] = zer_zer_locus
    f_alls['t'] = zer_one_locus

    m_alls['x'] = zer_one_locus
    m_alls['p'] = zer_one_locus
    m_alls['t'] = zer_zer_locus

    return f_alls, m_alls

def initialise_population(n, f_alls, m_alls):

    #to make n the number of males = number of females
    n = int(n/2)
    fems, mals = [], []

    fem_bird = Bird(f_alls['x'], f_alls['p'], f_alls['t'], 'F')
    mal_bird = Bird(m_alls['x'], m_alls['p'], m_alls['t'], 'M')

    for i in range(n):
        fems.append(fem_bird)
        mals.append(mal_bird)
    return fems, mals

def reached_maturity(n, f_birds, m_birds):

    f_reached, m_reached = [], []

    for i in range(int(n/2)):

        fb, mb = f_birds[i], m_birds[i]
        fp, mp = fb.not_reach_maturity(), mb.not_reach_maturity()
        fr, mr = random.uniform(0,1), random.uniform(0,1)

        if fr>fp: f_reached.append(fb)
        if mr>mp: m_reached.append(mb)

    return f_reached, m_reached

def meet_pairs(f_birds, m_birds):

    possible_pairs, S = [], 0
    for fb in f_birds:
        for mb in m_birds:

            mb_t = mb.ornament_contrib()
            mb_f, fb_f = mb.fitness(), fb.fitness()
            meet_prob = (1-mb_t)*mb_f*fb_f

            possible_pairs.append({'f':fb, 'm':mb, 'meet':meet_prob})
            S += meet_prob

    for pair in possible_pairs: pair['meet'] = pair['meet']/S
    return possible_pairs

def pick_random_pair(possible_pairs):

    roll = random.uniform(0,1)
    track, index, num_pairs = 0.0, 0, len(possible_pairs)
    for i in range(num_pairs):
        if roll <= (track + possible_pairs[i]['meet']):
            index = i
            break
        else: track += possible_pairs[i]['meet']
    return possible_pairs[index]

def offspring_genders(n):

    half = int(n/2)
    fs, ms = ['F']*half, ['M']*half
    fs.extend(ms)
    random.shuffle(fs)
    return fs

def exp_term(f, m):
    alpha = 0.5
    return np.exp(alpha*f.choosiness()*m.ornament_contrib()*m.fitness())

def exp_denominator(pair, m_birds):

    summat, f = 0.0, pair['f']
    for m in m_birds: summat += exp_term(f, m)
    return summat

def mating_probability(pair, m_birds):

    f, m = pair['f'], pair['m']
    numrt = exp_term(f, m)
    denmnt = exp_denominator(pair, m_birds)
    return numrt/denmnt

def get_offspring(pair, m_birds, gen):

    roll = random.uniform(0,1)
    matp = mating_probability(pair, m_birds)
    if matp > roll: return None

    offspring = pair['f'].mate(pair['m'], gen)
    return offspring

def propagate(n, f_birds, m_birds):

    f_birds, m_birds = reached_maturity(n, f_birds, m_birds)
    possible_pairs = meet_pairs(f_birds, m_birds)
    gen_order = offspring_genders(n)

    f_offspring, m_offspring, crt_num = [], [], 0
    while crt_num < n:

        pair = pick_random_pair(possible_pairs)
        gen = gen_order[crt_num]

        offspring = get_offspring(pair, m_birds, gen)
        if offspring is None: continue

        if gen == 'F': f_offspring.append(offspring)
        else: m_offspring.append(offspring)
        crt_num = crt_num + 1

    return f_offspring, m_offspring

def plot_beaksizes(n, beakszs, i):

    plt.hist(beakszs, color = 'blue', bins = int(n/5))
    plt.xlim([1.5,6.5])
    plt.ylim([0,n])
    filename = './tempdir/dist' + str(i) + '.png'

    plt.savefig(filename)
    plt.close()

def make_gif(num_generations):

    with imageio.get_writer('mygif.gif', mode='I') as writer:
        for i in range(num_generations):
            filename = './tempdir/dist' + str(i) + '.png'
            image = imageio.imread(filename)
            writer.append_data(image)

            os.remove(filename)

def plot_mean_var(means, vars, num_generations):

    plt.plot(means, c='r', label='mean beak size')
    plt.plot(vars, c='b', label='variance of beak size')
    plt.legend()
    plt.savefig('meanvarbeaksize.png')
    plt.close()

def get_beaksizes(n, f_birds, m_birds):

    half, beakszs = int(n/2), []
    for i in range(half):
        beakszs.append(f_birds[i].beak_size())
        beakszs.append(m_birds[i].beak_size())
    return beakszs

def evolution(n, f_birds, m_birds):

    num_generations = 200
    means, vars = [], []

    for i in range(num_generations):

        beakszs = get_beaksizes(n, f_birds, m_birds)
        mu, sig = np.mean(beakszs), np.var(beakszs)
        means.append(mu)
        vars.append(sig)
        plot_beaksizes(n, beakszs, i)

        f_birds, m_birds = propagate(n, f_birds, m_birds)

    make_gif(num_generations)
    plot_mean_var(means, vars, num_generations)


n_loci, n_popl = 20, 100
fem_alls, mal_alls = generate_alleles(n_loci)
Fs, Ms = initialise_population(n_popl, fem_alls, mal_alls)
evolution(n_popl, Fs, Ms)
