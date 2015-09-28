h = init_figure('comp vs incomp');
plot_time_elec(stat);

% get topo timewindows
ntopo = 6;
twin  = get_time_windows(stat, 0.05, ntopo);
twin.times = round(twin.times * 1000); % to ms

% create topo axes
uplim = 0.5;
hlims = [0.08, 0.05, 0.08];
ax    = toporow_create(h.fig, hlims, uplim, ntopo);

% create topo in each ax:
locs = get_relevant_locs(EEG, stat);
plot_topo_slices(stat, twin, ax, locs);

% two more axes
erp{1} = give_erp(EEG, [], 'cued_comp');
erp{2} =give_erp(EEG, [], 'cued_incomp');

figure;

subplot(2,1,1);
pos = get_cluster(stat, 0.05, 'pos');
plot_cluster_erp(pos, erp, EEG.times)

subplot(2,1,2);
neg = get_cluster(stat, 0.05, 'neg');
plot_cluster_erp(neg, erp, EEG.times);
