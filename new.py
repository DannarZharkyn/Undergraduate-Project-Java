import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Animated Hospital Queue Simulation")

# Controls
arrival_rate = st.slider("Arrival rate λ (patients/hour)", 1.0, 80.0, 20.0)
info_workers = st.slider("Information desk workers", 1, 4, 2)
nurse_workers = st.slider("Nurses", 1, 5, 3)
doctor_workers = st.slider("Doctors", 1, 5, 2)

sim_hours = st.slider("Simulation time (hours)", 1, 8, 4)
speed = st.slider("Animation speed", 0.01, 0.3, 0.05)

p1 = st.slider("Dropout after info desk", 0.0, 0.5, 0.2)
p2 = st.slider("Dropout after nurse", 0.0, 0.8, 0.5)

run = st.button("Run animation")

# Layout positions
x_entry = 0
x_info = 3
x_nurse = 7
x_doctor = 11
x_exit = 14

dt = 1 / 60      # 1 minute
steps = int(sim_hours / dt)

# Service times in hours
info_service = 3 / 60
nurse_service = 7 / 60
doctor_service = 12 / 60

if run:
    placeholder = st.empty()

    patients = []
    next_id = 0

    info_servers = [None] * info_workers
    nurse_servers = [None] * nurse_workers
    doctor_servers = [None] * doctor_workers

    q_info = []
    q_nurse = []
    q_doctor = []

    served_doctor = 0
    left_after_info = 0
    left_after_nurse = 0

    for step in range(steps):
        t = step * dt

        # arrivals
        num_arrivals = np.random.poisson(arrival_rate * dt)
        for _ in range(num_arrivals):
            patients.append({
                "id": next_id,
                "stage": "to_info",
                "x": x_entry,
                "y": 0,
                "service_done": None
            })
            next_id += 1

        # move arrivals to info queue
        for p in patients:
            if p["stage"] == "to_info":
                p["x"] += 0.3
                if p["x"] >= x_info - 1:
                    p["stage"] = "q_info"
                    q_info.append(p["id"])

        # assign info servers
        for i in range(info_workers):
            if info_servers[i] is None and q_info:
                pid = q_info.pop(0)
                info_servers[i] = pid
                for p in patients:
                    if p["id"] == pid:
                        p["stage"] = "serving_info"
                        p["service_done"] = t + np.random.exponential(info_service)

        # complete info service
        for i, pid in enumerate(info_servers):
            if pid is not None:
                p = next(p for p in patients if p["id"] == pid)
                if t >= p["service_done"]:
                    info_servers[i] = None
                    if np.random.rand() < p1:
                        p["stage"] = "left"
                        left_after_info += 1
                    else:
                        p["stage"] = "to_nurse"
                        p["x"] = x_info + 0.5

        # move to nurse queue
        for p in patients:
            if p["stage"] == "to_nurse":
                p["x"] += 0.3
                if p["x"] >= x_nurse - 1:
                    p["stage"] = "q_nurse"
                    q_nurse.append(p["id"])

        # assign nurse servers
        for i in range(nurse_workers):
            if nurse_servers[i] is None and q_nurse:
                pid = q_nurse.pop(0)
                nurse_servers[i] = pid
                for p in patients:
                    if p["id"] == pid:
                        p["stage"] = "serving_nurse"
                        p["service_done"] = t + np.random.exponential(nurse_service)

        # complete nurse service
        for i, pid in enumerate(nurse_servers):
            if pid is not None:
                p = next(p for p in patients if p["id"] == pid)
                if t >= p["service_done"]:
                    nurse_servers[i] = None
                    if np.random.rand() < p2:
                        p["stage"] = "left"
                        left_after_nurse += 1
                    else:
                        p["stage"] = "to_doctor"
                        p["x"] = x_nurse + 0.5

        # move to doctor queue
        for p in patients:
            if p["stage"] == "to_doctor":
                p["x"] += 0.3
                if p["x"] >= x_doctor - 1:
                    p["stage"] = "q_doctor"
                    q_doctor.append(p["id"])

        # assign doctor servers
        for i in range(doctor_workers):
            if doctor_servers[i] is None and q_doctor:
                pid = q_doctor.pop(0)
                doctor_servers[i] = pid
                for p in patients:
                    if p["id"] == pid:
                        p["stage"] = "serving_doctor"
                        p["service_done"] = t + np.random.exponential(doctor_service)

        # complete doctor service
        for i, pid in enumerate(doctor_servers):
            if pid is not None:
                p = next(p for p in patients if p["id"] == pid)
                if t >= p["service_done"]:
                    doctor_servers[i] = None
                    p["stage"] = "exit"
                    served_doctor += 1

        # assign visual positions for queues
        for idx, pid in enumerate(q_info):
            p = next(p for p in patients if p["id"] == pid)
            p["x"] = x_info - 1.0 - 0.25 * idx
            p["y"] = 0

        for idx, pid in enumerate(q_nurse):
            p = next(p for p in patients if p["id"] == pid)
            p["x"] = x_nurse - 1.0 - 0.25 * idx
            p["y"] = 0

        for idx, pid in enumerate(q_doctor):
            p = next(p for p in patients if p["id"] == pid)
            p["x"] = x_doctor - 1.0 - 0.25 * idx
            p["y"] = 0

        # visual positions for servers
        for i, pid in enumerate(info_servers):
            if pid is not None:
                p = next(p for p in patients if p["id"] == pid)
                p["x"] = x_info
                p["y"] = 0.4 - 0.35 * i

        for i, pid in enumerate(nurse_servers):
            if pid is not None:
                p = next(p for p in patients if p["id"] == pid)
                p["x"] = x_nurse
                p["y"] = 0.5 - 0.35 * i

        for i, pid in enumerate(doctor_servers):
            if pid is not None:
                p = next(p for p in patients if p["id"] == pid)
                p["x"] = x_doctor
                p["y"] = 0.4 - 0.35 * i

        # plot
        fig, ax = plt.subplots(figsize=(11, 4))

        ax.set_xlim(-1, 15)
        ax.set_ylim(-2, 2)
        ax.axis("off")

        # arrows/path
        ax.plot([x_entry, x_exit], [0, 0], linestyle="--", linewidth=1)

        # boxes
        ax.add_patch(plt.Rectangle((x_info - 0.6, -0.8), 1.2, 1.6, fill=False, linewidth=2))
        ax.text(x_info, 1.05, "Info Desk", ha="center")

        ax.add_patch(plt.Rectangle((x_nurse - 0.6, -0.8), 1.2, 1.6, fill=False, linewidth=2))
        ax.text(x_nurse, 1.05, "Nurses", ha="center")

        ax.add_patch(plt.Rectangle((x_doctor - 0.6, -0.8), 1.2, 1.6, fill=False, linewidth=2))
        ax.text(x_doctor, 1.05, "Doctors", ha="center")

        ax.text(x_entry, -1.2, "Entry", ha="center")
        ax.text(x_exit, -1.2, "Exit", ha="center")

        # worker labels
        ax.text(x_info, -1.35, f"{info_workers} workers", ha="center")
        ax.text(x_nurse, -1.35, f"{nurse_workers} nurses", ha="center")
        ax.text(x_doctor, -1.35, f"{doctor_workers} doctors", ha="center")

        # dots
        active = [p for p in patients if p["stage"] not in ["left", "exit"]]
        xs = [p["x"] for p in active]
        ys = [p["y"] for p in active]
        ax.scatter(xs, ys, s=45)

        ax.set_title(
            f"t = {t:.2f} hr | Q info={len(q_info)} | Q nurse={len(q_nurse)} | Q doctor={len(q_doctor)}"
        )

        ax.text(
            0,
            1.6,
            f"Served by doctor: {served_doctor} | Left after info: {left_after_info} | Left after nurse: {left_after_nurse}",
            fontsize=10
        )

        placeholder.pyplot(fig)
        plt.close(fig)

        time.sleep(speed)