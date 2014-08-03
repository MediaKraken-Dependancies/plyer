from subprocess import Popen, PIPE
from plyer.facades import Battery


class OSXBattery(Battery):
    def _get_status(self):
        status = {"isCharging": None, "percentage": None}

        ioreg_process = Popen(["ioreg", "-rc", "AppleSmartBattery"],
                stdout=PIPE)
        output = ioreg_process.communicate()[0]

        if not output:
            return status

        IsCharging = MaxCapacity = CurrentCapacity = None
        for l in output.splitlines():
            if 'IsCharging' in l:
                IsCharging = l.rpartition('=')[-1].strip()
            if 'MaxCapacity' in l:
                MaxCapacity = float(l.rpartition('=')[-1].strip())
            if 'CurrentCapacity' in l:
                CurrentCapacity = float(l.rpartition('=')[-1].strip())

        if (IsCharging):
            status['isCharging'] = IsCharging == "Yes"

        if (CurrentCapacity and MaxCapacity):
            status['percentage'] = 100. * CurrentCapacity / MaxCapacity

        return status


def instance():
    return OSXBattery()
