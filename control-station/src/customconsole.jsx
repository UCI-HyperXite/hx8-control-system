import { Console, Hook, Unhook } from 'console-feed';
import { useEffect, useRef, useState } from 'react';

export function CustomConsole() {
  const [logs, setLogs] = useState([]);
  const consoleContainerRef = useRef(null);

  useEffect(() => {
    const hookedConsole = Hook(
      window.console,
      (log) => {
        setLogs((currLogs) => [...currLogs, log]);
        scrollToBottom();
      },
      false
    );

    return () => Unhook(hookedConsole);
  }, []);

  const scrollToBottom = () => {
    consoleContainerRef.current.scrollTop = consoleContainerRef.current.scrollHeight;
  };

  return (
    <div className="CustomConsole" style={{ height: '424px', overflowY: 'scroll' }} ref={consoleContainerRef}>
      <div style={{ color: 'white' }}>
        <Console logs={logs} />
      </div>
    </div>
  );
}

export default CustomConsole;
