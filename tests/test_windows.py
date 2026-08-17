import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

import leodock


@unittest.skipUnless(leodock.IS_WINDOWS, "Windows platform tests")
class WindowsPlatformTests(unittest.TestCase):
    def test_windows_runtime_paths_use_local_app_data(self):
        local = os.path.abspath(
            os.environ.get("LOCALAPPDATA")
            or os.path.join(os.path.expanduser("~"), "AppData", "Local"))
        self.assertEqual(leodock.DATA_DIR, os.path.join(local, "LeoDock"))
        self.assertEqual(leodock.LOGS_DIR, os.path.join(local, "LeoDock", "logs"))
        self.assertTrue(leodock.WINDOWS_CURRENT_USER_SID)

    def test_script_commands_use_native_windows_runtimes(self):
        with tempfile.TemporaryDirectory() as td:
            paths = {}
            for name in ("job.py", "job.ps1", "job.cmd", "job.js"):
                path = os.path.join(td, name)
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write("# test\n")
                paths[name] = path

            self.assertIn(sys.executable, leodock.command_for_script(paths["job.py"]))
            self.assertIn("powershell.exe", leodock.command_for_script(paths["job.ps1"]))
            self.assertIn("cmd.exe", leodock.command_for_script(paths["job.cmd"]).lower())
            self.assertEqual(leodock.command_for_script(paths["job.js"]),
                             "node " + subprocess.list2cmdline([paths["job.js"]]))

    def test_powershell_platform_commands_never_open_a_window(self):
        completed = subprocess.CompletedProcess([], 0, stdout="ok\n", stderr="")
        with mock.patch.object(
                leodock.shutil, "which", return_value=r"C:\Windows\powershell.exe"), \
                mock.patch.object(
                    leodock.subprocess, "run", return_value=completed) as run:
            self.assertEqual(leodock.run_powershell("Write-Output 'ok'"), "ok\n")

        self.assertEqual(
            run.call_args.kwargs["creationflags"], subprocess.CREATE_NO_WINDOW)

    def test_path_picker_uses_sta_and_serializes_interactive_dialogs(self):
        with mock.patch.object(leodock, "run_powershell", return_value="") as run:
            path, canceled = leodock.pick_path("dir")
        self.assertIsNone(path)
        self.assertTrue(canceled)
        self.assertEqual(run.call_args.kwargs["timeout"], leodock.PICKER_TIMEOUT)
        self.assertIn("-STA", run.call_args.kwargs["extra_args"])
        picker_script = run.call_args.args[0]
        self.assertIn("$owner.TopMost=$true", picker_script)
        self.assertIn("$owner.Location=[Windows.Forms.Cursor]::Position", picker_script)
        self.assertIn("$dialog.ShowDialog($owner)", picker_script)

        with leodock.WINDOWS_PICK_LOCK:
            with mock.patch.object(leodock, "run_powershell") as blocked:
                path, canceled = leodock.pick_path("dir")
        self.assertIsNone(path)
        self.assertTrue(canceled)
        blocked.assert_not_called()

    def test_listener_scan_parses_get_net_tcp_connection_rows(self):
        rows = [
            {"OwningProcess": 101, "LocalPort": 5173, "LocalAddress": "::1"},
            {"OwningProcess": 202, "LocalPort": 8000, "LocalAddress": "127.0.0.1"},
        ]
        with leodock.WINDOWS_SNAPSHOT_LOCK:
            leodock.WINDOWS_LISTENER_CACHE["mono"] = 0.0
        with mock.patch.object(leodock, "_powershell_json", return_value=rows):
            listeners = leodock.scan_listeners()
        self.assertEqual(listeners[(101, 5173)], {"::1"})
        self.assertEqual(leodock.listener_open_host(
            listeners, 5173, {101}), "localhost")

    def test_instance_lock_is_exclusive(self):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "leodock.lock")
            first = leodock.acquire_instance_lock(path)
            self.assertIsNotNone(first)
            try:
                self.assertIsNone(leodock.acquire_instance_lock(path))
            finally:
                leodock.release_instance_lock(first)
            second = leodock.acquire_instance_lock(path)
            self.assertIsNotNone(second)
            leodock.release_instance_lock(second)

    def test_started_task_is_identified_and_tree_is_stopped(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td, \
                mock.patch.object(leodock, "LOGS_DIR", td):
            command = subprocess.list2cmdline([
                sys.executable, "-c", "import time; time.sleep(30)"])
            app = {"id": "deadbeef", "command": command, "cwd": td}
            ok, error, proc, root_pid, token = leodock.start_app(app)
            self.assertTrue(ok, error)
            tracked = dict(app, lastPid=proc.pid, lastPgid=root_pid,
                           runToken=token)
            try:
                deadline = time.monotonic() + 5
                managed = []
                while time.monotonic() < deadline:
                    managed = leodock.managed_pids(tracked)
                    if proc.pid in managed:
                        break
                    time.sleep(0.1)
                self.assertIn(proc.pid, managed)
                stopped, error = leodock.stop_app_and_wait(
                    tracked, timeout=5)
                self.assertTrue(stopped, error)
                self.assertEqual(leodock._current_user_group_members(root_pid), [])
            finally:
                if leodock._current_user_group_members(root_pid):
                    leodock.stop_pid_tree(root_pid)

    def test_static_project_candidate_uses_current_python(self):
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "index.html"), "w", encoding="utf-8") as handle:
                handle.write("<!doctype html>")
            result, error = leodock.detect_project(td)
        self.assertIsNone(error)
        self.assertTrue(result["candidates"])
        candidate = result["candidates"][0]
        self.assertIn(sys.executable, candidate["command"])
        self.assertEqual(candidate["port"], 8000)

    def test_health_accepts_windows_acl_managed_storage(self):
        with tempfile.TemporaryDirectory() as td:
            config_path = os.path.join(td, "config.json")
            with mock.patch.multiple(
                    leodock, DATA_DIR=td, ICONS_DIR=os.path.join(td, "icons"),
                    LOGS_DIR=os.path.join(td, "logs"), CONFIG_PATH=config_path):
                os.mkdir(leodock.ICONS_DIR)
                os.mkdir(leodock.LOGS_DIR)
                cfg = leodock.Config(config_path)
                health = leodock.build_health(cfg)
        self.assertTrue(health["ok"], health["issues"])


if __name__ == "__main__":
    unittest.main()
