import numpy as np
import matplotlib.pyplot as plt

"""
The purpose of this script is to build a few chart to find out
how the new H1B rule proposed by White House on 11/30/2018 will
affect the chances for H1B applicants with US Master degree.

I'll potentially add how it affects other applicants
"""

MASTER_CAP = 20000
GENERAL_CAP = 65000

# ----- ANALYTICAL SOLUTION ----- #
def new_rule(college, master):
    first_chance = GENERAL_CAP / (college + master)
    if first_chance > 1:
        first_chance = 1
    master_left = master * (1 - first_chance)
    second_chance = MASTER_CAP / master_left
    if second_chance > 1:
        second_chance = 1
    overall_chance = first_chance + (1 - first_chance) * second_chance
    return overall_chance
    
def old_rule(college, master):
    first_chance = MASTER_CAP / master
    if first_chance > 1:
        first_chance = 1
    master_left = master - MASTER_CAP
    second_chance = GENERAL_CAP / (college + master_left)
    if second_chance > 1:
        second_chance = 1
    overall_chance = first_chance + (1 - first_chance) * second_chance
    return overall_chance

def master_chance(college, master):
    old_chance = old_rule(college, master)
    new_chance = new_rule(college, master)
    return old_chance, new_chance, new_chance - old_chance

# Create figure with matplotlib contourf
def create_figure(data, title):
    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(111)
    cs = ax.contourf(cc, mm, data*100)
    ax.set_xlabel('College Applicant Count')
    ax.set_ylabel('US-Master Applicant Count')
    ax.set_title(title)
    ax.grid(True)
    plt.colorbar(cs)
    fig.set_facecolor('lightgray')
    # plt.show()
    return fig

# Generate meshgrid of possible applicant makeup
college = np.arange(70000, 300000, 2500)
master = np.arange(20000, 120000, 1000)
cc, mm = np.meshgrid(college, master)

improvement = []
old_chance = []
new_chance = []
for c, m in zip(cc.ravel(), mm.ravel()):
    old, new, im = master_chance(c, m)
    old_chance.append(old)
    new_chance.append(new)
    improvement.append(im)

improven = np.array(improvement).reshape(cc.shape)
oldn = np.array(old_chance).reshape(cc.shape)
newn = np.array(new_chance).reshape(cc.shape)

myfig = create_figure(improven, "Percentage Chance improvement for master degree applicant")
myfig.savefig('improvement.png')
myfig = create_figure(oldn, "Percentage Acceptance for US Master degree holder, Old Rules")
myfig.savefig('old_chances.png')
myfig = create_figure(newn, "Percentage Acceptance for US Master degree holder, New Rules")
myfig.savefig('new_chances.png')

