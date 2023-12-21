import tired.command
import tired.logging


@dataclasses.dataclass
class TmuxPaneInfo:
    window_index: object = None
    window_name: object = None
    pane_current_path: object = None
    pane_current_command: object = None
    my_title: object = None
    pane_title: object = None


class TmuxSessions(dict):

    def register_pane(self, tmux_pane_info):
        key = tmux_pane_info.window_index
        if key not in self.keys():
            self[key] = list()

        self[key].append(tmux_pane_info)


def tmux_get_all_window_sessions() -> TmuxSessions:
    tmux_sessions = TmuxSessions()
    command = "tmux list-panes -a -F '#{window_index}----#{window_name}----#{pane_current_path}----#{pane_current_command}----#{@mytitle}----#{pane_title}'"
    panes = tired.command.get_output(command).strip()

    for pane_info in tired.parse.iterate_string_multiline(panes):
        pane_info = pane_info.strip()
        window_index, window_name, pane_current_path, pane_current_command, my_title, pane_title = pane_info.split("----")
        tmux_pane_info = TmuxPaneInfo(
            window_index=window_index,
            window_name=window_name,
            pane_current_path=pane_current_path,
            pane_current_command=pane_current_command,
            my_title=my_title,
            pane_title=pane_title,
        )
        tmux_sessions.register_pane(tmux_pane_info)

    tired.logging.debug("Tmux sessions", str(tmux_sessions))

    return tmux_sessions

