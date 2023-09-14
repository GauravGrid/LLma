export const colorScheme = {
    primary : '#2B3140',
    background : '#D0D1D2',
    menu_primary : '#97AABD',
    menu_secondary : '#535F7E'
}

import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    background: {
      default: '#D0D1D2',
    },
  },
});

export default theme;