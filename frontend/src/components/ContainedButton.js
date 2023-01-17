import * as React from 'react';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

export default function ContainedButtons(props) {
  return (
    <Stack direction="row" spacing={1}>
      <Button style={{ marginRight:10, marginLeft:10 }} variant="contained" onClick={props.onClick}>{props.value}</Button>
    </Stack>
  );
}