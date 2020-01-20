from mpl_toolkits.axes_grid1 import make_axes_locatable

def colorbar(mappable):
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="1%", pad=0.05)
    return fig.colorbar(mappable, cax=cax)



pct = df\
        .drop_duplicates(['Provider', 'TimePoint', 'TemplateDesc'])\
        .assign(NumRecs=1)\
        .groupby(['Provider', 'TemplateDesc'])['NumRecs'].sum() /\
      df\
        .drop_duplicates(['Provider', 'TimePoint', 'TemplateDesc'])\
        .assign(NumRecs=1)\
        .groupby(['Provider'])['NumRecs'].sum()

#pct is a pd.Series(data=['pct'], index=['Provider', 'Template'])

pct = pct*100

pct = pct[pct >= 1]

print(pct.max())
fillna_with = 0 #pct.max() + (pct.max()*.1)
new_ys = pct.unstack().index.tolist()
n_ys = len(new_ys)

new_xs = pct.unstack().columns.tolist()
n_xs = len(new_xs)

fig, ax = plt.subplots(figsize=(22, 10))
ax.set_facecolor('lightgray')
#im = ax.imshow(pct.unstack().fillna(fillna_with), cmap='hot_r', interpolation='nearest')
im = ax.imshow(pct.unstack(), cmap='hot_r', interpolation='nearest')

fig.colorbar(im)

for i in ax.get_yticks()[::1][1:-1]:
    ax.hlines(i+.4, 0, n_xs-0.5, color='gray', linewidth=1)

plt.yticks(np.arange(0, n_ys, 1), fontsize=12)
plt.xticks(np.arange(0, n_xs, 1), fontsize=12)

ax.set_yticklabels(new_ys)
ax.set_xticklabels(new_xs, rotation=90)

ax.set_title("Each Provider's Percent of Templetes Used\n(displaying only 1% or greater types uesd.)", color='DarkRed', fontsize=18)

fig.savefig(r'results\Percent of Templete Clicks by Provider.png', bbox_tight=True, bbox_inches='tight')