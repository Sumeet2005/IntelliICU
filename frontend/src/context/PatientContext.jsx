import {
    createContext,
    useContext,
    useMemo,
    useState,
    useCallback,
} from "react";

const PatientContext = createContext(null);

export function PatientProvider({ children }) {

    const [patientsList, setPatientsList] = useState([]);

    const [selectedPatient, setSelectedPatient] = useState(null);

    const clearSelectedPatient = useCallback(() => {
        setSelectedPatient(null);
    }, []);

    const value = useMemo(() => ({
        patientsList,
        setPatientsList,

        selectedPatient,
        setSelectedPatient,

        clearSelectedPatient,
    }), [
        patientsList,
        selectedPatient,
        clearSelectedPatient,
    ]);

    return (
        <PatientContext.Provider value={value}>
            {children}
        </PatientContext.Provider>
    );
}

export function usePatient() {

    const context = useContext(PatientContext);

    if (!context) {
        throw new Error(
            "usePatient must be used inside PatientProvider."
        );
    }

    return context;
}