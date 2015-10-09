function EEG = senofag_recode_marks(EEG, after_resp)

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
all_i = 0;

% add fields to EEG.events
addfields = {'cond', 'choice', 'hand', 'corr'};
for f = addfields
    EEG.event(1).(f{1}) = [];
end

newevent = struct('type', cell(length(EEG.event),1), ...
    'latency', [], 'urevent', [], 'cond', [], 'choice', [], ...
    'hand', [], 'corr', []);
for t = 1:length(targ)
    % find all targets of given type:
    t_ind = find(strcmp(targ{t}, tps));
    c = targ_cond{t};
    for i = t_ind
        all_i = all_i + 1;
        % check next event:
        num = str2double(regexp(tps{i+1}, '[0-9]+', ...
            'once', 'match'));
        row = find(num == numtype);
        
        % fill current event:
        EEG.event(i) = fill_event(EEG.event(i), c, ...
            type2info, row);
        
        % fill next event
        EEG.event(i+1) = fill_event(EEG.event(i+1), 'effect', ...
            type2info, row);
        
        % add newevent based on the latency of effect
        newevent(all_i) = fill_event(EEG.event(i+1), 'reaction', ...
            type2info, row);
        newevent(all_i).latency = EEG.event(i+1).latency - ...
            round(after_resp(all_i) / 4);
    end
end
newevent = newevent(1:all_i);
EEG.event = [EEG.event, newevent'];

% sort all events by latency:
lat = [EEG.event.latency];
[~, ord] = sort(lat);
EEG.event = EEG.event(ord);

end

% merge all_new_event, and add

function s = fill_event(s, c, type2info, row)
s.type = [c, '_', type2info{row,2}];
s.cond = type2info{row,2};
s.choice = c;
s.hand = type2info{row,3};
s.corr = type2info{row,4};
end