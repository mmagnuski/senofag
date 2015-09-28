function EEG = senofag_recode_marks(EEG)

% currently recodes
% DIN2 and DIN3 events to
% cued_... and free_...
% where ... can be:
% comp, incomp or neut (or error noresp)
% following fields are added to target marks:
% choice = [free/cued];
% hand   = [left/right];
% cond   = [comp, incomp, neut]
% corr   = [1 0 NaN]

tps = {EEG.event.type};
targ = {'DIN2', 'DIN3'};
targ_cond = {'cued', 'free'};
type2info = {...
	10, 'noresp', '', NaN;...
	11, 'error',  '', false;...
	12, 'comp', 'left', true;...
	13, 'comp', 'right', true;...
	14, 'incomp', 'right', true;...
	15, 'incomp', 'left', true;...
	16, 'neut', 'right', true;...
	17, 'neut', 'left', true};
numtype = cell2mat(type2info(:,1));
all_new_event = cell(1,2);
all_i = 0
for t = 1:length(targ)
	% find all targets of given type:
	t_ind = find(strcmp(targ{t}, tps));
    newevent = struct('type', cell(length(t_ind),1), ...
        'latency', [], 'cond', [], 'choice', [], ...
        'hand', [], 'corr', []);
	c = targ_cond{t};
	for i = t_ind
		all_i = all_i + 1;
		% check next event:
		num = str2num(regexp(tps{i+1}, '[0-9]+', ...
			'once', 'match'));
		row = find(num == numtype);

		% fill current event:
		EEG.event(i) = fill_event(EEG.event(i), c, ...
			type2info, row);
        
        % fill next event
        EEG.event(i+1) = fill_event(EEG.event(i+1), 'effect',
        	type2info, row);
        
        % add newevent based on the latency of effect
        newevent(i) = fill_event(EEG.event(i+1), 'reaction',
        	type2info, row);
        newevent(i).latency = EEG.event(i+1).latency - ...
        	after_resp(all_i);
	end
	all_new_event{t} = newevent;
end

% merge all_new_event, and add

function ev = fill_event(s, c, type2info, row)
    s.type = [c, '_', type2info{row,2}];
    s.cond = type2info{row,2};
    s.choice = c;
    s.hand = type2info{row,3};
    s.corr = type2info{row,4};
end