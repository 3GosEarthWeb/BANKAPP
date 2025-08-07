import { useState } from 'react';

const useToggle = (initialValue = false) => {
  const [state, setState] = useState(initialValue);
  return [state, toggle];
};

export default useToggle;

