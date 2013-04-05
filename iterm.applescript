on run argv
	set title to item 1 of argv
	set dir to item 2 of argv
	tell application "iTerm"
		if (exists current terminal) then
			set _term to current terminal
		else
			set _term to (make new terminal)
		end if
		tell _term
			set _session to (launch session "Default Session")
			tell _session
				write text " cd " & dir & "; clear;"
			end tell
		end tell
	end tell
end run
