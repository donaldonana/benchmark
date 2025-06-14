## GreenFaaS

To support the proposed idea, we begin by outlining the motivation behind the project. We implement alternatives to a state-of-the-art benchmark, deploying them on Apache OpenWhisk. During execution, we monitor energy consumption, execution time, and result quality for each alternative.

## How to Run the Experiment

1. **Set Up the Configuration**  
      **a.** We use Ansible to automatically configure the runtime environment. To begin, you need to install Ansible:

   ```shell
   python3 -m pip -V venv
   source ./venv/bin/activate
   python3 -m pip install ansible
   ```

      **b.** We then need to modify the ansible inventories **inventory.yaml** which contain all the  **IP address** or fully **qualified domain name (FQDN)** of each  node in runtime environment. Modify the **ansible_host** key in that file, and write the correct IP for each compute and storage node. 
 
   ```bash
   ansible compute -m ping -i inventory.yaml
   ```

      **c.** Set up all  compute node. The following command, use the ansible playbook **compute.yaml**  to install openwhisk,  set the device core frequency in the max frequence, ... 

   ```bash
   ansible-playbook -i inventory.yaml compute.yaml
   ```

      **d.** Set up all storage node. The following command, use the ansible playbook **SAIO.yaml**  to install and configure SAIO in the storage node. 

   ```bash
   ansible-playbook -i inventory.yaml SAIO.yaml
   ```

 

2. **Run each benchmark**  

   ....




 